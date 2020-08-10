from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required
from markupsafe import Markup
from Apps.article.form import PostForm, CommentForm
from sqlalchemy import func
from Apps.article.model import Comment, ArticleType, Article
from extents import db

article_bp = Blueprint('article', __name__)


@article_bp.route('/archives')
def archives():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    post_years = []

    articles = Article.query.order_by(Article.timestamp.desc())
    # years = Article.query.order_by(Article.timestamp.desc()).filter(extract('year', Article.timestamp))

    # archives = db.session.query(extract('year', Article.timestamp).label('year'),
    #                             extract('month', Article.timestamp).label('month')).distinct().all()[::-1]
    archives = db.session.query(func.date_format(Article.timestamp, '%Y-%m').label('date'),
                                func.count('*').label('cnt')).distinct().group_by('date').all()[::-1]
    # years = db.session.query(func.date_format(Article.timestamp, '%Y').label('year')).distinct().group_by('year').all()[::-1]
    # 归档获取月份

    # for year in years:
    #     post_years.append(year.timestamp.strftime("%Y"))
    # post_years = list(set(post_years))
    # post_years.sort(reverse=True)
    # return render_template('article/archives.html', articles=posts, post_years=post_years)
    return render_template('article/archives.html', articles=articles, archives=archives)


@article_bp.route('/category/<int:category_id>', methods=['GET', 'POST'])
def show_category(category_id):
    category = ArticleType.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Article.query.with_parent(category).order_by(Article.timestamp.desc()).paginate(page, per_page)
    types = ArticleType.query.all()
    return render_template('article/category.html', category=category, pagination=pagination, types=types)


@article_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Article()
        post.title = form.title.data
        post.type_id = form.category.data
        post.content = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('New post have posted!', 'primary')
        return redirect(url_for('article.show_post', pid=post.id))
    return render_template('article/new_post.html', form=form)


@article_bp.route('/post/<int:pid>', methods=['GET', 'POST'])
def show_post(pid):
    post = Article.query.get_or_404(pid)
    form = CommentForm()

    if form.validate_on_submit():
        if request.args.get('reply'):  # 如果获取到评论回复id，则添加评论回复id
            replied_id = request.args.get('reply')
            comment = Comment(comment=form.body.data,
                              email=form.email.data,
                              author=form.author.data,
                              article_id=pid,
                              reviewed=1,
                              replied_id=replied_id)
        else:
            comment = Comment(comment=form.body.data,
                              email=form.email.data,
                              author=form.author.data,
                              article_id=pid,
                              reviewed=1)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', 'primary')
        return redirect(url_for('article.show_post', pid=pid))
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.desc()).paginate(
        page=page, per_page=5)
    # 通过父引用获取分页，降序排列
    comments = pagination.items
    return render_template('article/post.html', post=post, form=form, comments=comments, pagination=pagination)


@article_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    flash(Markup('Reply to  ' +
                 comment.author +
                 '<a class="float-right" href="' +
                 url_for('article.show_post', pid=comment.article_id, reply=0) +
                 '#author' +
                 '">Cancel</a>'), 'light')
    return redirect(url_for('article.show_post', pid=comment.article_id, reply=comment.id) + '#author')

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from markupsafe import Markup

from Apps.article.form import PostForm, CommentForm
from Apps.user.model import User

from Apps.article.model import Comment, ArticleType, Article
from extents import db

article_bp = Blueprint('article', __name__)


@article_bp.route('/achieves')
def achieves():
    import datetime
    from datetime import date

    start = date(year=datetime.datetime.now().year, month=1, day=1)
    end = date(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=30)

    posts = Article.query.filter(Article.create_time <= end).filter(Article.create_time >= start)
    return render_template('article/archives.html', posts=posts)


@article_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Article()
        post.title = form.title.data
        post.type_id = form.category.data
        post.content = form.body.data
        db.session.commit()
        flash('New post have posted!')
        return redirect(url_for('user.index'))
    form.category.data = ArticleType.query.order_by(ArticleType.id)
    return render_template('article/new_post.html', form=form)


@article_bp.route('/post/<int:pid>', methods=['GET', 'POST'])
def show_post(pid):
    post = Article.query.get_or_404(pid)
    form = CommentForm()

    if form.validate_on_submit():
        if request.args.get('reply') == 1:
            replied_id = request.args.get('reply')
            comment = Comment(comment=form.body.data,
                              email=form.email.data,
                              author=form.author.data,
                              article_id=pid,
                              replied_id=replied_id)
        else:
            comment = Comment(comment=form.body.data,
                              email=form.email.data,
                              author=form.author.data,
                              article_id=pid)

        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('article.show_post', pid=pid))
    page = request.args.get('page', 1, type=int)
    # if page == -1:
    #     page = (post.comments.count() - 1)
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.create_time.asc()).paginate(
        page=page, per_page=5)
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

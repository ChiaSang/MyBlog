from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from Apps.article.form import PostForm, CommentForm
from Apps.user.model import User

from Apps.article.model import Comment, ArticleType, Article
from extents import db

article_bp = Blueprint('article', __name__)


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
    # cu_user = User.query.get(current_user.id)
    # return render_template('article/new_post.html', user=cu_user)
    form.category.data = ArticleType.query.order_by(ArticleType.id)
    return render_template('article/new_post.html', form=form)


@article_bp.route('/post/<int:pid>', methods=['GET', 'POST'])
def show_post(pid):
    post = Article.query.get_or_404(pid)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.body.data,
                          email=form.email.data,
                          author=form.author.data,
                          article_id=pid)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('article.show_post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    # if page == -1:
    #     page = (post.comments.count() - 1)
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.create_time.asc()).paginate(
        page=page, per_page=2)
    comments = pagination.items
    return render_template('article/post.html', post=post, form=form, comments=comments, pagination=pagination)

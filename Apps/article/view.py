from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from Apps.article.form import PostForm
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


@article_bp.route('/post', methods=['GET', 'POST'])
def post():
    pid = request.args.get('pid', type=int)
    post_detail = Article.query.get(pid)
    comments = Comment.query.get(pid)
    return render_template('article/post.html', post=post_detail, comments=comments)


@article_bp.route('/comment', methods=['GET', 'POST'])
def comment():
    pid = request.args.get('pid', type=int)
    post_detail = Article.query.get(pid)
    comments = Comment.query.get(pid)
    return render_template('article/post.html', post=post_detail, comments=comments)

from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from Apps.user.model import User

from Apps.article.model import Article, Comment

article_bp = Blueprint('article', __name__)


@article_bp.route('/post', methods=['GET', 'POST'])
def post():
    pid = request.args.get('pid', type=int)
    post_detail = Article.query.get(pid)
    comments = Comment.query.get(pid)
    return render_template('article/post.html', post=post_detail, comments=comments)


@article_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    cu_user = User.query.get(current_user.id)
    return render_template('article/new_post.html', user=cu_user)

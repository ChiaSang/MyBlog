from flask import Blueprint, request, render_template

from Apps.article.model import Article, ArticleType

article_bp = Blueprint('article', __name__, url_prefix='/article')

from urllib.parse import urlencode
import requests
import json


@article_bp.route('/post', methods=['GET', 'POST'])
def post():
    pid = request.args.get('pid')
    post_detail = Article.query.get(pid)
    post_type = ArticleType.query.all()
    return render_template('article/post.html', post=post_detail, type=post_type)

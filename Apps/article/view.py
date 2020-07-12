from flask import Blueprint

article_bp = Blueprint('article', __name__, url_prefix='/article')


@article_bp.route('/post', methods=['GET', 'POST'])
def post():
    pass

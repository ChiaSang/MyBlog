import calendar
from collections import defaultdict, Counter
from datetime import datetime, date, timedelta

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required
from markupsafe import Markup
from Apps.article.form import PostForm, CommentForm
from sqlalchemy import extract, func, and_, cast
from Apps.article.model import Comment, ArticleType, Article
from extents import db

article_bp = Blueprint('article', __name__)


@article_bp.route('/archives')
def archives():
    post_years = []
    articles = Article.query.order_by(Article.timestamp.desc())
    years = Article.query.order_by(Article.timestamp.desc()).filter(extract('year', Article.timestamp))
    for year in years:
        post_years.append(year.timestamp.strftime("%Y"))
    print(post_years)
    post_years = list(set(post_years))
    post_years.sort(reverse=True)
    return render_template('article/archives.html', articles=articles, post_years=post_years)


@article_bp.route('/archive/<int:year>/<int:month>')
def archive_month(year, month):
    """
    按照日期对post进行归档展示
    """
    post_date = date(year, month, 1)  # 日期区间,天数默认为1
    days_in_month = calendar.monthrange(post_date.year, post_date.month)
    end_date = post_date + timedelta(days=days_in_month[1])  # 获取当前月份的天数
    iso_lower_date = post_date.isoformat()
    iso_upper_date = end_date.isoformat()  # 格式化日期为iso格式 e.g. 2020-12-22
    articles = db.session.query(Article).filter(Article.timestamp.between(iso_lower_date, iso_upper_date))
    return render_template('article/archive.html', articles=articles, year=year, month=month)


@article_bp.route('/archive/<int:year>')
def archive_year(year):
    """
    按照日期对post进行归档展示
    """
    post_lower_date = date(year, 1, 1)  # 日期区间,月份，天数默认为1
    post_upper_date = post_lower_date + timedelta(days=365)
    iso_lower_date = post_lower_date.isoformat()
    iso_upper_date = post_upper_date.isoformat()  # 格式化日期为iso格式 e.g. 2020-12-22
    articles = db.session.query(Article).filter(Article.timestamp.between(iso_lower_date, iso_upper_date))
    return render_template('article/archive.html', articles=articles, year=year)


@article_bp.route('/archive')
def show_archives():
    post = db.session.query(Article.timestamp).all()[::-1]
    d = defaultdict(list)
    for i in post:
        d[i.timestamp.year].append(i.timestamp.month)
    # add the monthly counts by counting the instances of month number.
    date_dict = {}
    for k, v in d.items():
        date_dict[k] = Counter(v)
    total_dict = {}
    # add the monthly and yearly totals counts
    post_total = 0
    for key, value in date_dict.items():
        year_sum = 0
        for m, c in value.items():
            year_sum += c
            post_total += c
            total_dict[key] = year_sum
    # d = defaultdict(list)
    # for k in date_dict.items():
    #     for v in total_dict.items():
    #         d[k].append(v)
    return render_template('sidebar.html', date_dict=date_dict, total_dict=total_dict)


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

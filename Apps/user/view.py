import random

import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.globals import session, g
from flask_login import login_user, login_required, current_user, logout_user
from markupsafe import Markup
from sqlalchemy.exc import IntegrityError

from werkzeug.security import check_password_hash, generate_password_hash

# from Apps import user
from Apps.user.form import RegisterForm, LoginForm, EditProfileForm
from Apps.user.model import User

from sqlalchemy import or_

from extents import db, login
from Apps.article.model import ArticleType, Article, Comment
from faker import Faker

user_bp = Blueprint('user', __name__)

require_login_list = ['/usercenter', '/info', '/user/update', '/posts']


# if request_url in require_login_list:
#     id = session.get('uid')
#     if not id:
#         return render_template(url_for('user.user_login'))
#     else:
#         print("==============>")
#         user = User.query.get(int(session.get('uid')))
#         g.user = user


@user_bp.before_app_request
# @login_required
def before_request():
    if request.path in require_login_list:
        if current_user.is_authenticated:
            auth_user = User.query.get(current_user.id)
            g.user = auth_user

        # if session.get('uid'):
        #     print("==============>")
        #     user = User.query.get(int(session.get('uid')))
        #     g.user = user
        # if request.path in require_login_list:
        #     uid = session.get('uid')
        #     if not uid:
        #         return render_template('user/login.html')
        #     else:
        #         print("==============>")
        #         user = User.query.get(int(session.get('uid')))
        #         g.user = user
        #         print("@@@@@@@@@@", g.user)
        else:
            # form = LoginForm()
            return redirect(url_for('user.user_login'))


# 自己定义未登录的处理引擎
@login.unauthorized_handler
def unauthorized():
    return '未登入'


@user_bp.route('/')
def index():
    print("=====================主页=====================\n\n", session.get('_id'), session.get('user_id'))

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(-Article.timestamp).paginate(page=page, per_page=10)
    # type_num = Article.query.order_by(Article.type_id).all()
    types = ArticleType.query.all()
    # if current_user.is_authenticated:
    # #  request cookie to judge user whether login or not
    #     uid = request.cookies.get('uid')
    #     if session.get('uid'):
    #     index_uid = session.get('uid')
    #     user = User.query.get(int(index_uid))
    #     # print("**************", g.user)
    #     # 通过cookies判断首页登入状态
    # return render_template('index.html', username=current_user.name, types=types, pagination=pagination)
    # else:
    return render_template('index.html', types=types, pagination=pagination)


@user_bp.route('/register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        passwd = form.password.data
        user = User(email=email.lower(),
                    name=username,
                    passwd=generate_password_hash(passwd))
        db.session.add(user)
        db.session.commit()
        flash('You have register successed.')
        return redirect(url_for('user.user_login'))
    else:
        return render_template('user/register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(name=username).first()
        if user is not None and check_password_hash(user.passwd, password):
            login_user(user, remember=remember)
            flash('Logged in successfully.', 'primary')
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('user.index')
            return redirect(next)
        flash('Invalid username or password.', 'warning')
    return render_template('user/login.html', form=form)


@user_bp.route('/logout', methods=['GET', 'POST'])
@login_required
@login.needs_refresh_handler
def user_logout():
    logout_user()
    flash('You have been logged out.', 'primary')
    return redirect(url_for('user.index'))


#  =========================================================================
#  =========================================================================
#  =========================================================================
@user_bp.route('/delete', methods=['GET', 'POST'])
def user_delete():
    uid = request.args.get('id')
    User.query.filter_by(id=uid).delete()
    db.session.commit()
    return redirect(url_for('user.user_center'))


# 更新图片处理没有做
@user_bp.route('/update', methods=['GET', 'POST'])
def user_update():
    print("=====================更新=====================\n\n", session.get('_id'), session.get('user_id'))

    if request.method == 'POST':
        username = request.form.get('username')
        # phone = request.form.get('phone')
        uid = request.form.get('id')
        email = request.form.get('email')
        ch_user = User.query.get(uid)
        ch_user.name = username
        # ch_user.phone = phone
        ch_user.email = email
        db.session.commit()
        return redirect(url_for('user.user_info'))
    else:
        return render_template('user/update.html', user=g.user)


#  =========================================================================
@user_bp.route('/edit/<username>', methods=['GET', 'POST'])
@login_required
def user_info(username):
    # return render_template('user/info.html', form=g.user)
    form = EditProfileForm()
    if form.validate_on_submit():
        # user = User()
        current_user.name = form.username.data
        current_user.email = form.email.data
        current_user.blog_name = form.blog_name.data
        current_user.blog_sub_name = form.blog_sub_name.data
        db.session.commit()
        flash('Your profile has been updated.', 'primary')
        return redirect(url_for('user.user_info', username=current_user.name))
    form.username.data = current_user.name
    form.email.data = current_user.email
    form.blog_name.data = current_user.blog_name
    form.blog_sub_name.data = current_user.blog_sub_name
    return render_template('user/info.html', form=form)

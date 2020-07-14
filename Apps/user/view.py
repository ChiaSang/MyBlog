import random

import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.globals import session, g
from flask_login import login_user, login_required, current_user, logout_user
from markupsafe import Markup
from sqlalchemy.exc import IntegrityError

from werkzeug.security import check_password_hash, generate_password_hash

# from Apps import user
from Apps.user.form import RegisterForm, LoginForm
from Apps.user.model import User

from sqlalchemy import or_

from extents import db, login
from Apps.article.model import ArticleType, Article, Comment
from faker import Faker

user_bp = Blueprint('user', __name__)

require_login_list = ['/usercenter', '/info', '/user/update', '/posts']

fake = Faker('zh_CN')


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
            form = LoginForm()
            return render_template('user/login.html', form=form)


# 自己定义未登录的处理引擎
@login.unauthorized_handler
def unauthorized():
    return '未登入'


@user_bp.route('/')
# @login_required
def index():
    print("=====================主页=====================\n\n", session.get('_id'), session.get('user_id'))

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(-Article.create_time).paginate(page=page, per_page=5)
    type_num = Article.query.order_by(Article.type_id).all()
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
    return render_template('index.html', types=types, pagination=pagination, type_num=type_num)


@user_bp.route('/register', methods=['GET', 'POST'])
def user_regist():
    print("=====================注册=====================\n\n", session.get('_id'), session.get('user_id'))

    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    rform = RegisterForm()
    if rform.validate_on_submit():
        username = rform.username.data
        email = rform.email.data
        passwd = rform.password.data
        repasswd = rform.confirm.data
        phone = rform.phone.data
        user = User()
        user.name = username
        user.email = email
        user.passwd = generate_password_hash(passwd)
        user.phone = phone
        db.session.add(user)
        db.session.commit()
        # return redirect(url_for(user.user_center'))
        return redirect(url_for('user.index'))
    else:
        return render_template('user/register.html', form=rform)
        # return '密码不一致'
    # return render_template('user/register.html', form=rform)
    # if request.method == 'GET':
    #     rform = RegisterForm()
    #     if rform.validate_on_submit():
    #         return render_template('user/register.html', form=rform)
    #     else:
    #         return render_template('user/register.html', form=rform)
    # else:
    #     # return render_template('user/register.html')
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     passwd = request.form.get('password')
    #     repasswd = request.form.get('confirm')
    #     phone = request.form.get('phone')
    #     if User.query.filter_by(phone=phone) == phone:
    #         flash('手机号已经被注册')
    #         return redirect(url_for('user.user_regist'))
    #     elif passwd == repasswd:
    #         user = User()
    #         user.name = username
    #         user.email = email
    #         user.passwd = generate_password_hash(passwd)
    #         user.phone = phone
    #         db.session.add(user)
    #         db.session.commit()
    #         # return redirect(url_for(user.user_center'))
    #         return redirect(url_for('user.index'))
    #     else:
    #         return '密码不一致'


@user_bp.route('/usercenter')
@login_required
def user_center():
    print("=====================中心=====================\n\n", session.get('_id'), session.get('user_id'))

    # if session.get('uid'):
    if current_user.id:
        # seuid = session.get('uid')  # 返回为字符串
        # user = User.query.get(int(seuid))

        cu_user = User.query.get(current_user.id)
        return render_template('user/center.html', user=cu_user)
    else:
        return '未登入......'


# @user_bp.route('/login', methods=['GET', 'POST'])
# def user_login():
#     if request.method == 'POST':
#         username = request.form.get('user')
#         passwd = request.form.get('passwd')
#         users = User.query.filter_by(name=username)
#         for user in users:
#             if user.name == username:
#                 if check_password_hash(user.passwd, passwd):
#                     session['uid'] = user.id
#                     response = redirect(url_for('user.user_center'))
#                     #  set cookie to send user login status
#                     response.set_cookie('uid', str(user.id))
#                     return response
#                 else:
#                     return render_template('user/login.html', msg='信息有误!')
#         # else:
#         #     return 'User does not exist !'
#     return render_template('user/login.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    print("=====================登入=====================\n\n", session.get('_id'), session.get('user_id'))

    if current_user.is_authenticated:
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        louser = User.query.filter_by(name=username).first()
        if louser and check_password_hash(louser.passwd, password):
            login_user(louser, remember=remember)
            flash('Logged in successfully.')
            # flash(Markup('<div class="alert alert-dismissible alert-light">Logged in successfully.</div>'))
            # next = flask.request.args.get('next')
            # if next:
            #     return redirect(url_for(next))
            # return redirect(url_for('user.index'))
            return redirect(url_for('user.index'))
        # flash('errors')
    return render_template('user/login.html', form=form)


@user_bp.route('/logout', methods=['GET', 'POST'])
@login_required
@login.needs_refresh_handler
def user_logout():
    print("=====================退出=====================\n\n", session.get('_id'), session.get('user_id'))

    # del session['uid']
    # response = redirect(url_for('user.index'))
    # response.delete_cookie('uid')
    # return response
    logout_user()
    pagination = Article.query.order_by(-Article.create_time).paginate(page=1, per_page=5)
    types = ArticleType.query.all()
    return render_template('index.html', types=types, pagination=pagination)


@user_bp.route('/posts', methods=['GET', 'POST'])
@login_required
def posts_create():
    print("=====================创建=====================\n\n", session.get('_id'), session.get('user_id'))

    if request.method == 'POST':
        # uid = request.cookies.get('uid')
        if g.user:
            return 'yes'
    else:
        pass


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
        phone = request.form.get('phone')
        uid = request.form.get('id')
        email = request.form.get('email')
        ch_user = User.query.get(uid)
        ch_user.name = username
        ch_user.phone = phone
        ch_user.email = email
        db.session.commit()
        return redirect(url_for('user.user_info'))
    else:
        return render_template('user/update.html', user=g.user)


@user_bp.route('/search', methods=['GET', 'POST'])
def user_search():
    if request.method == 'POST':
        srkey = request.form.get('search')
        search_list = User.query.filter(or_(User.name.contains(srkey), User.phone.contains(srkey)))
        return render_template(url_for('user.user_info'), search_list=search_list)
    else:
        return 'search failed'


#  =========================================================================
@user_bp.route('/info', methods=['GET', 'POST'])
@login_required
def user_info():
    print("=====================信息=====================\n\n", session.get('_id'), session.get('user_id'))

    if current_user.id:
        return render_template('user/info.html', user=g.user)


#  =========================================================================
@user_bp.route('/nav')
def nav():
    return render_template('navbar.html')


@user_bp.route('/add')
def add():
    print("=====================添加=====================\n\n", session.get('_id'), session.get('user_id'))

    # ========================================
    db.drop_all()
    print("清楚成功!!!!!!!")
    db.create_all()
    print("创建成功!!!!!!!")
    admin = User(name='admin', email=fake.email(), passwd=generate_password_hash('chiasang'), phone='13255556666')
    db.session.add(admin)
    db.session.commit()
    count = 20
    category = ArticleType(type_name='Default')
    db.session.add(category)
    for i in range(count):
        category = ArticleType(type_name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    # ====
    for i in range(count):
        post = Article(
            title=fake.sentence(),
            content=fake.text(2000),
            type_id=ArticleType.query.get(random.randint(1, ArticleType.query.count())).id,
            love_num=random.randint(1, ArticleType.query.count()),
            click_num=random.randint(1, 100),
            create_time=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()
    # ====
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            comment=fake.sentence(),
            create_time=fake.date_time_this_year(),
            reviewed=True,
            article_id=Article.query.get(random.randint(1, Article.query.count())).id
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # unreviewed comments
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            comment=fake.sentence(),
            create_time=fake.date_time_this_year(),
            love_num=random.randint(1, ArticleType.query.count()),
            reviewed=False,
            article_id=Article.query.get(random.randint(1, Article.query.count())).id
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            comment=fake.sentence(),
            create_time=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            article_id=Article.query.get(random.randint(1, Article.query.count())).id
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            comment=fake.sentence(),
            create_time=fake.date_time_this_year(),
            reviewed=True,
            replied_id=Comment.query.get(random.randint(1, Comment.query.count())).id,
            article_id=Article.query.get(random.randint(1, Article.query.count())).id
        )
        db.session.add(comment)
    db.session.commit()
    flash('信息添加成功', 'info')
    return redirect(url_for('user.index'))

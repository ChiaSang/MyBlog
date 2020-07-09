# Define user view fun

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.globals import session, g

from werkzeug.security import check_password_hash, generate_password_hash

from Apps.user.form import RegisterForm
from Apps.user.model import User

from sqlalchemy import or_

# Create a blueprint and instantiated
from extents import db

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
def before_request():
    # if session.get('uid'):
    #     print("==============>")
    #     user = User.query.get(int(session.get('uid')))
    #     g.user = user
    if request.path in require_login_list:
        uid = session.get('uid')
        if not uid:
            return render_template('user/login.html')
        else:
            print("==============>")
            user = User.query.get(int(session.get('uid')))
            g.user = user
            print("@@@@@@@@@@", g.user)


@user_bp.route('/index')
def index():
    #  request cookie to judge user whether login or not
    uid = request.cookies.get('uid')
    if session.get('uid'):
        index_uid = session.get('uid')
        user = User.query.get(int(index_uid))
        # print("**************", g.user)
        # 通过cookies判断首页登入状态
        return render_template('index.html', user=user)
    else:
        return render_template('index.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def user_regist():
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
def user_center():
    if session.get('uid'):
        # seuid = session.get('uid')  # 返回为字符串
        # user = User.query.get(int(seuid))
        return render_template('user/center.html', user=g.user)
    else:
        return '未登入......'


@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('user')
        passwd = request.form.get('passwd')
        users = User.query.filter_by(name=username)
        for user in users:
            if user.name == username:
                if check_password_hash(user.passwd, passwd):
                    session['uid'] = user.id
                    response = redirect(url_for('user.user_center'))
                    #  set cookie to send user login status
                    response.set_cookie('uid', str(user.id))
                    return response
                else:
                    return render_template('user/login.html', msg='信息有误!')
        # else:
        #     return 'User does not exist !'
    return render_template('user/login.html')


@user_bp.route('/logout', methods=['GET', 'POST'])
def user_logout():
    del session['uid']
    response = redirect(url_for('user.index'))
    response.delete_cookie('uid')
    return response


@user_bp.route('/posts', methods=['GET', 'POST'])
def posts_create():
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
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        uid = request.form.get('id')
        email = request.form.get('email')
        user = User.query.get(uid)
        user.name = username
        user.phone = phone
        user.email = email
        db.session.commit()
        return redirect(url_for('user.user_info'))
    else:
        # uid = request.args.get('id')
        uid = g.user.id
        user = User.query.get(uid)
        return render_template('user/update.html', user=user)


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
def user_info():
    if session.get('uid'):
        return render_template('user/info.html', user=g.user)
#  =========================================================================
@user_bp.route('/nav')
def nav():
    return  render_template('navbar.html')
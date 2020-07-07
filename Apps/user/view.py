# Define user view fun
import hashlib

from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from Apps.user.model import User

from sqlalchemy import or_


# Create a blueprint and instantiated
from extents import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/index')
def index():
    #  request cookie to judge user whether login or not
    uid = request.cookies.get('uid')
    if uid:
        user = User.query.get(uid)
        return render_template('index.html', user=user)
    else:
        return render_template('index.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    # Create a register fun
    :return:
    """
    if request.method == 'GET':
        return render_template('user/register.html')
    print(request.form.get('user'))
    username = request.form.get('user')
    passwd = request.form.get('passwd')
    repasswd = request.form.get('repasswd')
    phone = request.form.get('phone')
    if username == 'admin':
        return '<br>System Reservation</br>'
    elif passwd == repasswd:
        user = User()
        user.name = username
        user.passwd = generate_password_hash(passwd)
        user.repass = generate_password_hash(passwd)
        user.phone = phone
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        return '密码不一致'


@user_bp.route('/usercenter')
def user_center():
    users = User.query.all()
    return render_template('user/center.html', users=users)


@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('user')
        passwd = request.form.get('passwd')
        users = User.query.filter_by(name=username)
        for user in users:
            if user.name == username:
                if check_password_hash(user.passwd, passwd):
                    response = redirect(url_for('user.user_center'))
                    #  set cookie to send user login status
                    response.set_cookie('uid', str(user.id), max_age=600)
                    return response
                else:
                    return render_template('user/login.html', msg='信息有误!')
        else:
            return 'User does not exist !'
    return render_template('user/login.html')


@user_bp.route('/delete', methods=['GET', 'POST'])
def user_delete():
    uid = request.args.get('id')
    User.query.filter_by(id=uid).delete()
    db.session.commit()
    return redirect(url_for('user.user_center'))


@user_bp.route('/update', methods=['GET', 'POST'])
def user_update():
    if request.method  == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        uid = request.form.get('id')
        user = User.query.get(uid)
        user.name = username
        user.phone = phone
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        uid = request.args.get('id')
        user = User.query.get(uid)
        return render_template('user/update.html', user=user)


@user_bp.route('/search', methods=['GET', 'POST'])
def user_search():
    if request.method  == 'POST':
        srkey = request.form.get('search')
        search_list = User.query.filter(or_(User.name.contains(srkey), User.phone.contains(srkey)))
        return render_template('user/center.html', search_list = search_list)
    else:
        return 'search failed'


@user_bp.route('/posts', methods=['GET', 'POST'])
def posts_create():
    if request.method  == 'POST':
        uid = request.cookies.get('uid')
        if uid:
            return 'yes'
    else:
        pass

# Define user view fun
import hashlib

from flask import Blueprint, render_template, request, redirect, url_for

from Apps.user.model import User

from sqlalchemy import or_

# Create a blueprint and instantiated
from extents import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/index')
def index():
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
        user.passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
        user.repass = hashlib.md5(repasswd.encode('utf-8')).hexdigest()
        user.phone = phone
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        return '密码不一致'
    # return render_template('user/register.html')


@user_bp.route('/usercenter')
def user_center():
    users = User.query.all()
    return render_template('user/center.html', users=users)


@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('user')
        passwd = request.form.get('passwd')
        hash_passwd = hashlib.md5(passwd.encode('utf8')).hexdigest()
        users = User.query.filter_by(name=username)
        for user in users:
            if user.name == username:
                if user.passwd == hash_passwd:
                    return 'Login Success'
                else:
                    return render_template('user/login.html', msg='info Errors')
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



# Define user view fun
from flask import Blueprint, render_template, request, redirect

from Apps.user.model import User

# Create a blueprint and instantiated
from extents import db

user_bp = Blueprint('user', __name__)


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
        user.passwd = passwd
        user.repass =repasswd
        user.phone = phone
        db.session.add(user)
        db.session.commit()
        return 'ok'
    else:
        return '密码不一致'
    # return render_template('user/register.html')

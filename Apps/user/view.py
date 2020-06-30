# Define user view fun
from flask import Blueprint, render_template, request, redirect

from Apps.user.model import User

# Create a blueprint and instantiated
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
    user = request.form.get('user')
    passwd = request.form.get('passwd')
    repasswd = request.form.get('repasswd')
    if user == 'admin':
        return '<br>System Reservation</br>'
    elif passwd == repasswd:
        user = User(user, passwd)
        return 'ok'
    return render_template('user/register.html')

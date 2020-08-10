from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from Apps.article.form import PostForm
from Apps.user.form import RegisterForm, LoginForm, EditProfileForm
from Apps.user.model import User
from extents import db, login
from Apps.article.model import ArticleType, Article, Comment

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(-Article.timestamp).paginate(page=page, per_page=10)
    types = ArticleType.query.all()
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


@user_bp.route('/edit/<username>', methods=['GET', 'POST'])
@login_required
def user_info(username):
    form = EditProfileForm()
    if form.validate_on_submit():
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


@user_bp.route('/delete/comment/<int:cid>')
def comment_delete(cid):
    pid = request.args.get('pid')
    Comment.query.filter_by(id=cid).delete()
    db.session.commit()
    return redirect(url_for('article.show_post', pid=pid))


@user_bp.route('/delete/post/<int:pid>')
def post_delete(pid):
    Article.query.filter_by(id=pid).delete()
    db.session.commit()
    return redirect(url_for('article.archives'))


@user_bp.route('/delete/category/<int:tid>')
def category_delete(tid):
    ArticleType.query.filter_by(id=tid).delete()
    db.session.commit()
    return redirect(url_for('article.archives'))


@user_bp.route('/edit/post/<int:pid>', methods=['GET', 'POST'])
def edit_post(pid):
    form = PostForm()
    post = Article.query.get_or_404(pid)
    if form.validate_on_submit():
        post.title = form.title.data
        post.type_id = form.category.data
        post.content = form.body.data
        db.session.commit()
        flash('Edit Success!', 'primary')
        return redirect(url_for('article.show_post', pid=post.id))
    form.title.data = post.title
    form.category.data = post.type_id
    form.body.data = post.content
    db.session.add(post)
    db.session.commit()
    return render_template('user/edit_post.html', form=form)

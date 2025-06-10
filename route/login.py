from route import main_bp
from db.ops import get_user, register_user
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_security.utils import verify_password, hash_password
from route.forms import LoginForm, RegisterForm, ForgotPasswordForm

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = get_user(username)
        if user and verify_password(password, user.password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误', 'error')
    return render_template('login.html', form=form)

@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        username = form.username.data

        user = get_user(username)
        if user:
            flash('请联系管理员重置密码', 'info')
        else:
            flash('未找到该用户', 'error')

        return redirect(url_for('main.forgot_password'))

    return render_template('forget.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if get_user(username):
            flash('用户名已存在', 'error')
            return render_template('register.html', form=form)

        hashed_password = hash_password(password)
        user = register_user(username, hashed_password)

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

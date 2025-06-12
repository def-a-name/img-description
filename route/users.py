import os
from route import main_bp
from config import Config
from service.prompt import get_prompt_filename
from db.models import user_datastore
from db.ops import get_all_users, get_user_by_id, register_user, delete_user_by_id, change_user_password, update_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request
from route.forms import LoginForm, RegisterForm, ForgotPasswordForm

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = user_datastore.find_user(username=username)
        if user and check_password_hash(user.password, password):
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
        user = user_datastore.find_user(username=username)

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

        if user_datastore.find_user(username=username):
            flash('用户名已存在', 'error')
            return render_template('register.html', form=form)

        admin_token = form.admin_token.data
        if admin_token:
            if admin_token == Config.ADMIN_SECRET:
                admin_role = user_datastore.find_or_create_role(name='admin')
                user = register_user(username, generate_password_hash(password))
                user_datastore.add_role_to_user(user, admin_role)
                update_db()
            else:
                flash('管理员注册密钥错误', 'error')
                return render_template('register.html', form=form)
        else:
            user = register_user(username, generate_password_hash(password))

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/user-manage')
@login_required
def show_users():
    users = get_all_users()
    return render_template('users.html', users=users)

@main_bp.route('/add-user', methods=['POST'])
@login_required
def add_user():
    username = request.form['username']
    password = request.form['password']
    is_admin = 'is_admin' in request.form

    if user_datastore.find_user(username=username):
        flash('用户已存在', 'error')
        return redirect(url_for('main.show_users'))

    user = register_user(username, generate_password_hash(password))

    if is_admin:
        admin_role = user_datastore.find_or_create_role(name='admin')
        user_datastore.add_role_to_user(user, admin_role)

    update_db()
    flash('用户添加成功', 'success')
    return redirect(url_for('main.show_users'))

@main_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if delete_user_by_id(user_id):
        prompt_path = get_prompt_filename(user_id)
        if os.path.exists(prompt_path):
            try:
                os.remove(prompt_path)
            except Exception as e:
                flash(f'用户删除成功，但删除 prompt 历史文件时出错: {e}', 'error')
            else:
                flash('用户和 prompt 历史文件删除成功', 'success')
        else:
            flash('用户删除成功（未找到 prompt 历史文件）', 'success')
    else:
        flash('用户删除失败', 'error')
    return redirect(url_for('main.show_users'))

@main_bp.route('/change-password/<int:user_id>', methods=['POST'])
@login_required
def change_password(user_id):
    new_password = request.form['new_password']
    user = change_user_password(user_id, generate_password_hash(new_password))
    if user:
        flash('用户密码已修改', 'success')
    return redirect(url_for('main.show_users'))

@main_bp.route('/promote-user/<int:user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        admin_role = user_datastore.find_or_create_role(name='admin')
        user_datastore.add_role_to_user(user, admin_role)
        update_db()
        flash('用户已被设为管理员', 'success')
    return redirect(url_for('main.show_users'))

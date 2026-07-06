import datetime

import sqlalchemy as sa
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Введите почту и пароль', 'danger')
            return render_template('auth/login.html')

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        db_sess.close()

        if not user or not user.check_password(password):
            flash('Неверная почта или пароль', 'danger')
            return render_template('auth/login.html')

        session['user_id'] = user.id
        return redirect(url_for('chat.index'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_again = request.form.get('password_again', '')

        if not name or not email or not password:
            return render_template('auth/register.html', message="Заполните все обязательные поля")
        if password != password_again:
            return render_template('auth/register.html', message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == email).first():
            db_sess.close()
            return render_template('auth/register.html', message="Пользователь с таким email уже существует")

        db_sess.execute(
            sa.insert(User).values(
                name=name,
                email=email,
                hashed_password=generate_password_hash(password),
                created_date=datetime.datetime.now(),
            )
        )
        db_sess.commit()
        db_sess.close()

        flash('Аккаунт создан, войдите', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

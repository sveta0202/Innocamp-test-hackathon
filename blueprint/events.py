import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from data import db_session
from data.users import User
from data.events import Event

events_bp = Blueprint('events_bp', __name__, url_prefix='/events')


@events_bp.route('/create', methods=['GET', 'POST'])
def create():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.id == user_id).first()

    if not current_user:
        db_sess.close()
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        start_at_raw = request.form.get('start_at', '').strip()
        end_at_raw = request.form.get('end_at', '').strip()
        member_emails_raw = request.form.get('member_emails', '').strip()

        if not title or not start_at_raw:
            flash('Заполни название и дату начала', 'danger')
            users = db_sess.query(User).order_by(User.name).all()
            response = render_template('events/create.html', users=users)
            db_sess.close()
            return response

        try:
            start_at = datetime.datetime.fromisoformat(start_at_raw)
            end_at = datetime.datetime.fromisoformat(end_at_raw) if end_at_raw else None
        except ValueError:
            flash('Неверный формат даты', 'danger')
            users = db_sess.query(User).order_by(User.name).all()
            response = render_template('events/create.html', users=users)
            db_sess.close()
            return response

        if end_at and end_at < start_at:
            flash('Дата окончания не может быть раньше даты начала', 'danger')
            users = db_sess.query(User).order_by(User.name).all()
            response = render_template('events/create.html', users=users)
            db_sess.close()
            return response

        event = Event(
            title=title,
            description=description,
            start_at=start_at,
            end_at=end_at,
            creator_id=current_user.id,
        )

        event.members.append(current_user)

        if member_emails_raw:
            emails = [email.strip() for email in member_emails_raw.split(',') if email.strip()]
            users_to_add = db_sess.query(User).filter(User.email.in_(emails)).all()
            existing_ids = {user.id for user in event.members}

            for user in users_to_add:
                if user.id not in existing_ids:
                    event.members.append(user)

        db_sess.add(event)
        db_sess.commit()
        db_sess.close()

        flash('Событие создано', 'success')
        return redirect(url_for('calendar_bp.index'))

    users = db_sess.query(User).order_by(User.name).all()
    response = render_template('events/create.html', users=users)
    db_sess.close()
    return response
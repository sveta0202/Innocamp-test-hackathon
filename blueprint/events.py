import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from data import db_session
from data.users import User
from data.events import Event

events_bp = Blueprint('events_bp', __name__, url_prefix='/events')

VALID_CATEGORIES = {'meeting', 'personal', 'work', 'important', 'other'}


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
        location = request.form.get('location', '').strip()
        category = request.form.get('category', 'other').strip()
        is_important = bool(request.form.get('important'))
        notify_minutes = 15 if request.form.get('notify') else None
        member_emails_raw = request.form.get('member_emails', '').strip()

        # The quick-add panel and modal send a separate date + time field;
        # the standalone create page can also send one combined datetime-local field.
        event_date = request.form.get('event_date', '').strip()
        event_time = request.form.get('event_time', '').strip()
        start_at_raw = request.form.get('start_at', '').strip()

        if category not in VALID_CATEGORIES:
            category = 'other'

        def _form_error(message):
            flash(message, 'danger')
            users = db_sess.query(User).order_by(User.name).all()
            response = render_template('events/create.html', users=users)
            db_sess.close()
            return response

        if not title:
            return _form_error('Заполни название события')

        try:
            if event_date:
                time_part = event_time or '00:00'
                start_at = datetime.datetime.fromisoformat(f'{event_date}T{time_part}')
            elif start_at_raw:
                start_at = datetime.datetime.fromisoformat(start_at_raw)
            else:
                return _form_error('Укажи дату начала')
        except ValueError:
            return _form_error('Неверный формат даты')

        event = Event(
            title=title,
            description=description,
            location=location or None,
            category=category,
            is_important=is_important,
            notify_minutes=notify_minutes,
            start_at=start_at,
            end_at=None,
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

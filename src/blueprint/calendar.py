import sqlalchemy.orm as orm
from flask import Blueprint, render_template, redirect, url_for, session

from data import db_session
from data.users import User

calendar_bp = Blueprint('calendar_bp', __name__, url_prefix='/calendar')


@calendar_bp.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    db_sess = db_session.create_session()
    user = db_sess.query(User).options(
        orm.joinedload(User.events)
    ).filter(User.id == user_id).first()

    if not user:
        db_sess.close()
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))

    events = sorted(user.events, key=lambda e: e.start_at)
    response = render_template('calendar/index.html', user=user, events=events)
    db_sess.close()
    return response
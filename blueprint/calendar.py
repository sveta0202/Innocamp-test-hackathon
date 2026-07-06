import calendar
import datetime

import sqlalchemy.orm as orm
from flask import Blueprint, render_template, redirect, url_for, session, request

from data import db_session
from data.users import User

calendar_bp = Blueprint('calendar_bp', __name__, url_prefix='/calendar')

MONTH_NAMES_RU = [
    '', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
]

# calendar.Calendar with firstweekday=0 starts weeks on Monday (ПН),
# matching the ПН..ВС header in the template.
_CAL = calendar.Calendar(firstweekday=0)


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

    today = datetime.date.today()
    try:
        year = int(request.args.get('year', today.year))
        month = int(request.args.get('month', today.month))
        datetime.date(year, month, 1)
    except (ValueError, TypeError):
        year, month = today.year, today.month

    events_by_day = {}
    for event in user.events:
        events_by_day.setdefault(event.start_at.date(), []).append(event)
    for day_events in events_by_day.values():
        day_events.sort(key=lambda e: e.start_at)

    weeks = []
    for week in _CAL.monthdatescalendar(year, month):
        week_cells = []
        for day_date in week:
            week_cells.append({
                'date': day_date,
                'day': day_date.day,
                'in_month': day_date.month == month,
                'is_today': day_date == today,
                'events': events_by_day.get(day_date, []),
            })
        weeks.append(week_cells)

    prev_month = month - 1 or 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    response = render_template(
        'calendar/index.html',
        user=user,
        weeks=weeks,
        month_name=MONTH_NAMES_RU[month],
        year=year,
        month=month,
        prev_year=prev_year, prev_month=prev_month,
        next_year=next_year, next_month=next_month,
        today=today,
    )
    db_sess.close()
    return response

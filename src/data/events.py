import datetime
import sqlalchemy
import sqlalchemy.orm as orm

from .db_session import SqlAlchemyBase

event_members = sqlalchemy.Table(
    'event_members',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True),
    sqlalchemy.Column('event_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('events.id'), primary_key=True),
)


class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    start_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    end_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    creator = orm.relationship('User', foreign_keys=[creator_id])
    members = orm.relationship('User', secondary='event_members', back_populates='events')
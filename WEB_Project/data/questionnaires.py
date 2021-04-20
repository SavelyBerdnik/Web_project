import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Questionnaires(SqlAlchemyBase):
    __tablename__ = 'questionnaires'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    content = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)

    code = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    page_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

from sqlalchemy import Column, Integer, Text
from .db_session import SqlAlchemyBase


class Connection(SqlAlchemyBase):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    ip = Column(Text)
    port = Column(Integer)
    auth = Column(Text)
    pem = Column(Text)
    user = Column(Text)
    password = Column(Text)

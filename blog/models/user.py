from sqlalchemy import Column, String, Integer

from blog import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    username = Column(String(50), unique=True)
    nickname = Column(String(50))
    password = Column(String(100))
    avatar = Column(String(200))

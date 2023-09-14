import aiohttp_sqlalchemy as ahsa

from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

from config import SessionMaker


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)

    metadata = metadata


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True)
    title = Column(String(32), index=True)
    description = Column(Text)
    created_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')

    metadata = metadata


async def db_context(app):
    ahsa.setup(app, [ahsa.bind(SessionMaker), ])
    await ahsa.init_db(app, metadata)
    yield

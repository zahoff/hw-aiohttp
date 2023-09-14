import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_URI = 'sqlite+aiosqlite:///' + os.path.join(basedir, 'sqlite3.db')

engine = create_async_engine(SQLITE_URI)
SessionMaker = sessionmaker(engine, AsyncSession)
session = SessionMaker()

import sqlalchemy

from app.deps import get_settings

boilerplate_engine = sqlalchemy.create_engine(get_settings().BOILERPLATE_DATABASE_URI, pool_pre_ping=True)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "postgresql://neondb_owner:jHdqIzbMG43S@ep-tight-poetry-a51ypzfn.us-east-2.aws.neon.tech/neondb?sslmode=require&options=project%3Dep-tight-poetry-a51ypzfn"

engine = create_engine(DATABASE_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class QRData(Base):
  __tablename__ = 'qrdata'
  id = Column(Integer, primary_key=True)
  data = Column(String, unique=True)


def init_db():
  Base.metadata.create_all(bind=engine)

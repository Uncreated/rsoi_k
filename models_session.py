from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import config, datetime


engine = create_engine(config.SQLALCHEMY_SESSION_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
															autoflush=False,
															bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
	
class Session(Base):
	__tablename__ = 'session'
	id = Column(Integer, primary_key = True)
	access_token = Column(String(64), unique = True);
	account_id = Column(Integer());
	
	def __init__(self, access_token = None, account_id = None):
		self.access_token = access_token
		self.account_id = account_id
		
	def __repr__(self):
		return '<User(%s,%s,%s)>' % (self.id,\
														self.access_token,\
														self.account_id)
	
	def serialize(self):
		return {'id': self.id,
					'access_token': self.access_token,
					'account_id': self.account_id}

def init_db():
	Base.metadata.create_all(bind=engine)
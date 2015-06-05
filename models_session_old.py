from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import config, datetime

engine = create_engine(config.SQLALCHEMY_SESSION_URI, convert_unicode=True)
dbm_session = scoped_session(sessionmaker(autocommit=False,
																autoflush=False,
																bind=engine))
Base = declarative_base()
Base.query = dbm_session.query_property()

def init_dbm():
	Base.metadata.create_all(bind=engine)
	print 'Base init!!!'
	q = dbm_session.query(Session).all()
	print q
	print '\n\n'

class Session(Base):
	__tablename__ = 'session'
	id = Column(Integer, primary_key = True)
	accessToken = Column(String(64), unique = True)
	creationDate = Column(DateTime)
	
	account_id = Column(Integer)
	
	def __init__(self, accessToken = None, creationDate = None):
		self.accessToken = accessToken
		self.creationDate = creationDate
		
	def __repr__(self):
		return '<Session(%s,%s,%s)>' % (self.id, self.creationDate, self.account_id)
		
	def serialize(self):
		return {
			'id': self.id, 
			'creationDate': str(self.creationDate),
			'account_id': self.account_id
		}
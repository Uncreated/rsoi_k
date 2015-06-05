from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import config, datetime


engine = create_engine(config.SQLALCHEMY_ACCOUNTS_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
															autoflush=False,
															bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
	
class Account(Base):
	__tablename__ = 'account'
	id = Column(Integer, primary_key = True)
	login = Column(String(32), unique = True);
	password = Column(String(32));
	name = Column(String(16), unique = True)
	
	session_id = Column(Integer)
	
	def __init__(self, login, password):
		self.login = login
		self.password = password
		
	def __repr__(self):
		return '<User(%s,%s,%s,%s)>' % (self.id,\
									self.login,\
									self.password,\
									self.session_id)
	
	def serialize(self):
		return {'id': self.id,
					'login': self.login,
					'password': self.password,
					'session_id': self.session_id}

def init_db():
	Base.metadata.create_all(bind=engine)
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import config, datetime


engine = create_engine(config.SQLALCHEMY_PURCHASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
															autoflush=False,
															bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Purchase(Base):
	__tablename__ = 'purchase'
	id = Column(Integer, primary_key = True)
	items = Column(String(1024))
	count = Column(Integer)
	status = Column(Integer)
	account_id = Column(Integer)
	
	def __init__(self, items = ''):
		self.items = items
		self.count = 0
		self.status = config.PURCHASE_STATUS_COLLECTING
	
	def __repr__(self):
		return '<Purchase(%s,[%s],%s,%s,%s)>' % (self.id,\
										self.items,\
										self.count,\
										self.status,\
										self.account_id)
										
	def serialize(self):
		return {'id': self.id,
				'items': self.items,
				'count': self.count,
				'status': self.status,
				'account_id': self.account_id}

def init_db():
	Base.metadata.create_all(bind=engine)
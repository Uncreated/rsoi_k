from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import config, datetime


engine = create_engine(config.SQLALCHEMY_ITEMS_URI, convert_unicode = True)
db_session = scoped_session(sessionmaker(autocommit = False,
															autoflush = False,
															bind = engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Item(Base):
	__tablename__ = 'item'
	
	id = Column(Integer, primary_key = True)
	name = Column(String(64))
	params = Column(String(1024))
	price = Column(Integer)
	
	def __init__(self, name, price, params = []):
		self.name = name
		self.params = params
		self.price = price
	
	def __repr__(self):
		return '<Item(%s,%s,[%s], %d)>' % (self.id,\
																self.name,\
																self.params,\
																self.price)
	
	def serialize(self):
		return {'id': self.id,
					'name': self.name,
					'params': self.params,
					'price': self.price}
				
def init_db():
	Base.metadata.create_all(bind = engine)
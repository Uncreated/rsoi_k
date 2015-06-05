from flask import *
from sqlalchemy import *
import config

app = Flask(__name__)
app.config.from_object('config')

import datetime, os, random, config, glib, json
from models_items import *

def getItemById(id):
	if id and id >= 0:
		item = db_session.query(Item).filter(Item.id == id).first()
		return item
	return None

@app.route('/item/<int:id>', methods = ['GET'])
def getItem(id = None):
	item = getItemById(id)
	if item:
		dict = {'item':item.serialize()}
		return Response(json.dumps(dict), 200)
	return Response(None, 400)

@app.route('/items', methods = ['GET'])
def getItems():
	ids = request.args.get('ids')
	if ids:
		ids = ids.split(',')
		if ids:
			items = []
			for id in ids:
				item = getItemById(id)
				if item:
					items.append(item.serialize())
			dict = {'items':items}
			if dict:
				return Response(json.dumps(dict), 200)
	return Response(None, 400)
	
@app.route('/search', methods = ['GET'])
def check():
	searchRequest = request.args.get('searchRequest')
	if searchRequest:
		page = request.args.get('page')
		perPage = request.args.get('perPage')
		typeSearch = request.args.get('typeSearch')
		
		if not page:
			page = 1
		page = glib.getInteger(page)
		if not perPage:
			perPage = config.PER_PAGE_DEFAULT
		perPage = glib.getInteger(perPage, min = 1, max = config.PER_PAGE_MAX)
		
		words = searchRequest.split(' ')
		conditions = []
		for word in words:
			conditions.append(Item.name.ilike('%{}%'.format(word)))
		
#pagination not working
		if typeSearch and typeSearch == 'OR':
			items = db_session.query(Item).filter(or_(*conditions)).offset((page - 1) * perPage).limit(perPage).all()
		else:
			items = db_session.query(Item).filter(and_(*conditions)).offset((page - 1) * perPage).limit(perPage).all()
		arr = []
		for item in items:
#need call serialize_light or serialize
			dict = {'id':item.id, 'name':item.name, 'price':item.price}# 'params':item.params
			arr.append(item.serialize())
		dict = {'items':arr}
		return Response(json.dumps(dict), 200)
	else:
		info='return first elements'
	return Response(None, 400)
	
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

app.run('127.0.0.1', debug=True, port=config.ports['items'])
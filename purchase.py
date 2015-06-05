from flask import *
from sqlalchemy import *
import config

app = Flask(__name__)
app.config.from_object('config')

import datetime, os, random, config, glib, json
from models_purchase import *

def moveItem(add = None, remove = None):
	code = 200
	if add or remove:
		dict = glib.jsonToDict(request.data)
		if dict:
			userId = dict.get('userId')
			itemId = dict.get('itemId')
			if userId and itemId:
				purchase = db_session.query(Purchase).filter(Purchase.account_id == userId, 
															Purchase.status == config.PURCHASE_STATUS_COLLECTING).first()
				if purchase or add:
					if not purchase:
						purchase = Purchase()
						purchase.status = config.PURCHASE_STATUS_COLLECTING
						purchase.account_id = userId
						db_session.add(purchase)
					if purchase.items:
						items = purchase.items.split(',')
					else:
						items = []
					if add:
						if purchase.count >= config.PURCHASE_MAX_ITEMS - 1:
							code = 411
						else:
							items.append(str(itemId))
					else:
						items.remove(str(itemId))
					purchase.items = ','.join(items)
					purchase.count = len(items)
					print purchase.items
					db_session.commit()
					return Response(None, code)
	return Response(None, 400)

@app.route('/itemAdd', methods = ['POST'])
def itemAdd():
	return moveItem(add = True)

@app.route('/itemDelete', methods = ['DELETE'])
def itemDelete():
	return moveItem(remove = True)
	
@app.route('/getItems/<int:userId>', methods = ['GET'])
def getItems(userId = None):
	if userId :
		purchase = db_session.query(Purchase).filter(Purchase.account_id == userId, 
													Purchase.status == config.PURCHASE_STATUS_COLLECTING).first()
		if purchase:
			dict = {'items': purchase.items}
			return Response(json.dumps(dict), 200)
	return Response(None, 400)
	
@app.route('/getPurchase/<int:userId>', methods = ['GET'])
def getPurchase(userId = None):
	if userId :
		page = glib.getInteger(request.args.get('page'))
		if not page:
			page = 1
		count = db_session.query(Purchase).filter(Purchase.account_id == userId, 
																	Purchase.status == config.PURCHASE_STATUS_DELIVERY_DONE).count()
		if count:
			purchase = db_session.query(Purchase).filter(Purchase.account_id == userId, 
																			Purchase.status == config.PURCHASE_STATUS_DELIVERY_DONE).offset(count - page).first()
			if purchase:
				dict = {'items': purchase.items, 'purchaseId':purchase.id, 'count':count}
				print purchase.items
				return Response(json.dumps(dict), 200)
	return Response(None, 400)
	
@app.route('/getStatus/<int:userId>', methods = ['GET'])
def getStatus(userId = None):
	if userId:
		purchase = db_session.query(Purchase).filter(Purchase.account_id == userId).first()
		if purchase:
			dict = {'status':purchase.status}
			return Response(json.dumps(dict), 200)
	return Response(None, 400)
	
@app.route('/changeStatus', methods = ['PUT'])
def changeStatus():
	dict = glib.jsonToDict(request.data)
	if dict:
		userId = dict.get('userId')
		status = dict.get('status')
		if userId:
			purchase = db_session.query(Purchase).filter(Purchase.account_id == userId).first()
			if purchase:
				purchase.status = status
				db_session.commit()
				return Response(None, 200)
	return Response(None, 400)
	
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

app.run('127.0.0.1', debug=True, port=config.ports['purchase'])
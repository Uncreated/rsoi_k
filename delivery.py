from flask import *
from sqlalchemy import *
import config

app = Flask(__name__)
app.config.from_object('config')

import datetime, os, random, config, glib, json
from models_purchase import *

@app.route('/delivery', methods = ['POST'])
def setDelivery():
	dict = glib.jsonToDict(request.data)
	if dict:
		userId = dict.get('userId')
		if userId:
			purchase = db_session.query(Purchase).filter(Purchase.account_id == userId, Purchase.status == config.PURCHASE_STATUS_PAYMENT_DONE).first()
			if purchase:
				purchase.status = config.PURCHASE_STATUS_DELIVERY_DONE
				db_session.commit()
				return Response(None, 200)
	return Response(None, 400)

app.run('127.0.0.1', debug=True, port=config.ports['delivery'])
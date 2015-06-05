CSRF_ENABLED = True
SECRET_KEY = 'N720S-129DK-Z2K49-ZMK29'

loc_host = 'http://127.0.0.1:'
ports = {'frontend': 5000, 'session': 5001, 'purchase': 5002, 'payment': 5003, 'delivery': 5004, 'items': 5005}
addrs = {'frontend': loc_host + str(ports['frontend']),\
			'session': loc_host + str(ports['session']),\
			'purchase': loc_host + str(ports['purchase']),\
			'payment': loc_host + str(ports['payment']),\
			'delivery': loc_host + str(ports['delivery']),\
			'items': loc_host + str(ports['items'])}

PER_PAGE_DEFAULT = 10
PER_PAGE_MAX = 50

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ACCOUNTS_URI = 'sqlite:///' + os.path.join(basedir, 'db/accounts.db')
SQLALCHEMY_PURCHASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/purchase.db')
SQLALCHEMY_SESSION_URI = 'sqlite:///session.db'
SQLALCHEMY_ITEMS_URI = 'sqlite:///' + os.path.join(basedir, 'db/items.db')

PURCHASE_STATUS_COLLECTING = 1
PURCHASE_STATUS_PAYMENT = 2
PURCHASE_STATUS_PAYMENT_DONE = 3
PURCHASE_STATUS_DELIVERY = 4
PURCHASE_STATUS_DELIVERY_DONE = 5
PURCHASE_MAX_ITEMS = 100

TOKEN_LENGTH = 54
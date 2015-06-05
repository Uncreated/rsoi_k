from flask import *
from sqlalchemy import *
from redis import Redis
import config

app = Flask(__name__)
app.config.from_object('config')
app.config['REDIS_QUEUE_KEY'] = 'SESSION_INMEMORY'

redis = Redis()

import datetime, os, random, config, glib, json
from models_accounts import *
#from models_session import *
	
def cutToken(accessToken):
	if accessToken:
		ln = len(accessToken)
		if ln>config.TOKEN_LENGTH:
			point = ln - config.TOKEN_LENGTH
			id = accessToken[:point]
			token = accessToken[point:]
			return id, token
	return None, None
	
def checkToken(accessToken = None):
	if accessToken:
		id, token = cutToken(accessToken)
		if id and token:
			value = redis.get(id)
			if value and value == token:
				return id, token
	return None, None
	
@app.route('/check', methods = ['GET'])
def check():
	id, token = checkToken(request.args.get('accessToken'))
	if id and token:
		return Response(None, 200)
	return Response(None, 400)
	
@app.route('/userId', methods = ['GET'])
def userId():
	id, token = checkToken(request.args.get('accessToken'))
	if id and token:
		dict = {'userId':id}
		return Response(json.dumps(dict), 200)
	return Response(None, 400)
	
@app.route('/login', methods = ['POST'])
def login():
	info = None
	dict = glib.jsonToDict(request.data)
	if dict:
		login = dict.get('login')
		password = dict.get('password')
		if login and password:
			account = db_session.query(Account).filter(Account.login == login, 
																		Account.password == password).first()
			if account:
				id = str(account.id)
				accessToken = redis.get(id)
				if not accessToken:
					accessToken = glib.createToken(config.TOKEN_LENGTH)
					redis.set(id, accessToken)
				dict = {'accessToken':id + accessToken}
				return Response(json.dumps(dict), 200)
			info = json.dumps({'info':'Account not found. Check your login and password.'})
	return Response(info, 400)

@app.route('/logout', methods = ['POST'])
def logout():
	dict = glib.jsonToDict(request.data)
	if dict:
		accessToken = dict.get('accessToken')
		id, token = checkToken(accessToken)
		if id and token and redis.get(id) == token:
			redis.delete(id)
			return Response(None, 200)
	return Response(None, 400)
	
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()
	
print '\n\n\n\n\n\n\n\n\n\n\n'
	
app.run('127.0.0.1', debug=True, port=config.ports['session'])
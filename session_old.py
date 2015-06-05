from flask import *
from sqlalchemy import *
import config

app = Flask(__name__)
app.config.from_object('config')

import datetime, os, random, config, glib, json
from models_accounts import *
from models_session import *
	
@app.route('/check', methods = ['GET'])
def check():
	accessToken = request.args.get('accessToken')
	if accessToken:
		if db_session.query(Session).filter(Session.accessToken == accessToken).first():
			return Response(None, 200)
	return Response(None, 400)
	
@app.route('/userId', methods = ['GET'])
def userId():
	accessToken = request.args.get('accessToken')
	if accessToken:
		session = db_session.query(Session).filter(Session.accessToken == accessToken).first()
		if session:
			dict = {'userId':session.account_id}
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
				session = db_session.query(Session).filter(Session.account_id == account.id).first()
				if not session:
					session = Session()
					session.account_id = account.id
					db_session.add(session)
					account.session_id = session
					db_session.commit()
				session.accessToken = glib.createToken(44, account.id)
				session.creationDate = datetime.datetime.utcnow()
				db_session.commit()
				dict = {'accessToken' : session.accessToken}
				return Response(json.dumps(dict), 200)
			info = json.dumps({'info':'Account not found. Check your login and password.'})
	return Response(info, 400)

@app.route('/logout', methods = ['POST'])
def logout():
	dict = glib.jsonToDict(request.data)
	if dict:
		accessToken = dict.get('accessToken')
		if accessToken:
			session = db_session.query(Session).filter(Session.accessToken==accessToken).first()
			if session:
				db_session.delete(session)
				db_session.commit()
				return Response(None, 200)
	return Response(None, 400)
	
@app.teardown_appcontext
def shutdown_session(exception=None):
#	db_session.remove()
	db_session.remove()

@app.route('/try')
def tryFunc():
	q = db_session.query(Session).all()
	print q
	return Response(None, 200)
	
print '\n\n\n\n\n\n\n\n\n\n\n'
	
app.run('127.0.0.1', debug=True, port=config.ports['session'])
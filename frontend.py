from flask import *
from config import *

app = Flask(__name__)
app.config.from_object('config')

import datetime, os, random, config, json
import requests
from forms import *
from glib import *

def checkLogin(cookies):
	accessToken = cookies.get('accessToken')
	if accessToken:
		response = glib.requestGet('session', 'check', params = {'accessToken':accessToken})
		if response.status_code == 200:
			return True
	return False

def getUserId(cookies):
	accessToken = cookies.get('accessToken')
	if accessToken:
		response = glib.requestGet('session', 'userId', params = {'accessToken':accessToken})
		if response and response.status_code == 200:
			dict = glib.jsonToDict(response.text)
			if dict:
				userId = dict.get('userId')
				if userId:
					return userId
	return None

@app.route('/hello')
def helloPage():
	return 'HelloWorld!'

@app.route('/index', methods = ['GET'])
def homePageRedirect():
	return redirect('/')
	
@app.route('/', methods = ['GET'])
def homePage():
	authorized = checkLogin(request.cookies)
	return render_template('home.html', authorized = authorized)
	
@app.route('/search', methods = ['GET', 'POST'])
def searchPage():
	authorized = checkLogin(request.cookies)
	form = SearchForm()
	searchRequest = request.args.get('searchRequest')
	page = request.args.get('page')
	if form.validate_on_submit():
		searchRequest = str(form.keyword.data)
		return redirect(url_for('searchPage', searchRequest = searchRequest, page=1))
	if searchRequest:
		searchRequest = glib.getStringOnlyLetters(searchRequest)
		form.keyword.data = searchRequest
	page = request.args.get('page')
	perPage = request.args.get('perPage')
	response = glib.requestGet('items', 'search', params = {'searchRequest':searchRequest, 'page':page, 'perPage':perPage})
	items = None
	if response and response.status_code == 200:
		dict = glib.jsonToDict(response.text)
		if dict:
			items = dict.get('items')
#	items = [Item(1,'first item', 100), Item(2,'second item', 200), Item(3,'third item', 300)]
	return render_template('search.html', form = form, items = items, request = (searchRequest != None), authorized = authorized)
	
@app.route('/list', methods = ['GET'])
def listPage():
	return 'ListPage'
	
@app.route('/login', methods = ['GET', 'POST'])
def loginPage():
	if checkLogin(request.cookies):
		return redirect('/')
	form = LoginForm()
	if form.validate_on_submit():
		dict = {'login':str(form.email.data),\
					'password':str(form.password.data)}
		response = glib.requestPost('session', 'login', data = json.dumps(dict))
		if response and response.status_code == 200:
			dict = glib.jsonToDict(response.text)
			if dict:
				accessToken = dict.get('accessToken')
				if accessToken:
					redir = redirect('/')
					redir.set_cookie('accessToken', accessToken)
					return redir
				else:
					return render_template('login.html', form = form, g_error = dict.get('info'))
#what if response == False
		return render_template('login.html', form = form, g_error = 'Check data')
	return render_template('login.html', form = form)
	
@app.route('/logout', methods = ['GET'])
def logoutPage():
	authorized = checkLogin(request.cookies)
	if authorized:
		accessToken = request.cookies.get('accessToken')
		if accessToken:
			dict = {'accessToken':accessToken}
			resp = glib.requestPost('session', 'logout', data = json.dumps(dict))
	redir = redirect('/')
	redir.set_cookie('accessToken', '')
	return redir
	
@app.route('/item/<int:id>', methods = ['GET'])
def itemsPage(id = None):
	authorized = checkLogin(request.cookies)
	item = None
	if id and id >=0:
		response = glib.requestGet('items', 'item/' + str(id))
		if response and response.status_code == 200:
			dict = glib.jsonToDict(response.text)
			if dict:
				item = dict.get('item')
				if item:
					item['params'] = glib.getItemParams(item.get('params'))
	return render_template('item.html', item = item, authorized = authorized)

@app.route('/itemAdd/<int:id>', methods = ['POST'])
def itemAdd(id = None):
	authorized = checkLogin(request.cookies)
	if authorized:
		if id and id >= 0:
			userId = getUserId(request.cookies)
			if userId != None:
				dict = {'itemId':id, 'userId':userId}
				response = glib.requestPost('purchase', 'itemAdd', data = json.dumps(dict))
				if response:
					if response.status_code == 200:
						return Response(None, 200)
					elif response.status_code == 411:
						return Response(json.dumps({'Max items':config.PURCHASE_MAX_ITEMS}), 411)
	return Response(None, 400)
	
@app.route('/itemDelete/<int:id>', methods = ['GET'])
def itemDelete(id = None):
	authorized = checkLogin(request.cookies)
	if authorized:
		if id and id >= 0:
			userId = getUserId(request.cookies)
			if userId != None:
				dict = {'itemId':id, 'userId':userId}
				response = glib.requestDelete('purchase', 'itemDelete', data = json.dumps(dict))
				if response:
					if response.status_code == 200:
						return redirect('/buy')
						return Response(None, 200)
	return Response(None, 400)
	
@app.route('/buy', methods = ['GET', 'POST'])
def buyPage():
	items = []
	authorized = checkLogin(request.cookies)
	sum = None
	if authorized:
		userId = getUserId(request.cookies)
		if userId:
			response = glib.requestGet('purchase', 'getItems/' + str(userId))
			if response and response.status_code == 200:
				dict = glib.jsonToDict(response.text)
				if dict:
					s = dict.get('items')
					if s and s != '':
						response = glib.requestGet('items', 'items', params = {'ids':s})
						if response and response.status_code == 200:
							dict = glib.jsonToDict(response.text)
							if dict:
								items = dict.get('items')
								if items:
									sum = 0
									for item in items:
										sum += glib.getInteger(item.get('price'))
	return render_template('buy.html', items = items, authorized = authorized, sum = sum)
	
	
@app.route('/history', methods = ['GET'])
def historyPage():
	items = []
	authorized = checkLogin(request.cookies)
	count = None
	purchaseId = None
	if authorized:
		userId = getUserId(request.cookies)
		if userId:
			page = request.args.get('page')
			if not page:
				page = 1
			response = glib.requestGet('purchase', 'getPurchase/' + str(userId), params = {'page':page})
			if response and response.status_code == 200:
				dict = glib.jsonToDict(response.text)
				if dict:
					s = dict.get('items')
					count = glib.getInteger(dict.get('count'))
					purchaseId = glib.getInteger(page) #glib.getInteger(dict.get('purchaseId'))
					if s and s != '':
						response = glib.requestGet('items', 'items', params = {'ids':s})
						if response and response.status_code == 200:
							dict = glib.jsonToDict(response.text)
							if dict:
								items = dict.get('items')
	prevId = None
	nextId = None
	if count and purchaseId:
		if purchaseId > 0:
			prevId = purchaseId - 1
		if purchaseId < count :
			nextId = purchaseId + 1
	return render_template('history.html', items = items, authorized = authorized, prevId = prevId, nextId = nextId)
	
@app.route('/payment', methods = ['GET', 'POST'])
def payment():
	authorized = checkLogin(request.cookies)
	if authorized:
		if request.method == 'GET':
			return render_template('payment.html', form = Form())
		else:
			userId = getUserId(request.cookies)
			if userId:
				data = json.dumps({'userId':userId})
				response = glib.requestPost('payment', 'payment', data = data)
				if response and response.status_code == 200:
					response = glib.requestPost('delivery', 'delivery', data = data)
					if response and response.status_code == 200:
						return redirect('/buy')
	return redirect('/')
		
app.run('127.0.0.1', debug = True, port = config.ports['frontend'])
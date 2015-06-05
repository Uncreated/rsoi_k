import datetime, os, random, config, json
import requests, re

class Item():
	def __init__(self, id, name, price = None, info = None):
		self.id = id
		self.name = name
		self.price = price
		self.info = info

def createToken(length, id = None):
	src = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	token = ''
	i=0
	while i < length:
		token += src[random.randint(0,61)]
		i += 1
	if id:
		return str(id) + token
	return token
		
def getItemParams(params):
	if params:
		pairs = params.split(',')
		params = []
		for pair in pairs:
			list = pair.split(':')
			if len(list) == 2:
				params.append([list[0], list[1]])
	return params
		
def getInteger(value, min = None, max = None):
	if value:
		t = type(value)
		if t == str or t == unicode:
			try:
				value = int(value)
			except:
				value = 0
		if type(value) != int:
			value = 0
		if min and value < min:
			value = min
		if max and value > max:
			value = max
		return value
	return None
		
def getStringOnlyLetters(string):
	result = ""
	if string:
		reg = re.compile("[a-z A-Z]+")
		if reg:
			strings = reg.findall(string)
			for str in strings:
				result += str
	return result

def stringOnlyLetters(string):
	return stringEqualRegular("[a-zA-Z]+", string)

def stringEqualRegular(regular, string):
	if regular and string:
		reg = re.compile(regular)
		if reg:
			res = reg.findall(string)
			if res and len(res) == 1 and res[0] == string:
				return True
	return False

def jsonToDict(data):
	try:
		dict = json.loads(data)
		if not dict:
			return None
	except:
		return None
	return dict

def requestGet(name, api, params=None, headers=None):
	uri=config.addrs[name]+'/'+api
	return requests.get(uri, params=params, headers=headers)
	
def requestPost(name, api, data=None, params=None):
	return requests.post(config.addrs[name]+'/'+api,\
						params = params,\
						data = data,\
						headers = {'Content-Type': 'application/json'})
	
def requestDelete(name, api, data=None, params=None):
	return requests.delete(config.addrs[name]+'/'+api,\
							params = params,\
							data = data,\
							headers = {'Content-Type': 'application/json'})
#!/usr/bin/python3

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
#import hyvee_api as hyvee
import secrets
import bakers_api as bakers
import json

KEY_LENGTH = 45

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///keys.sqlite3"
db = SQLAlchemy(app)

class ApiObject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(KEY_LENGTH))

	def __init__(self, key):
		self.key = key

def generateAPIKey():
	return secrets.token_urlsafe(KEY_LENGTH)	

#@app.route("/check", methods=['POST'])
def isValidKey(k):
	#j = json.loads(request.data)

	a = ApiObject.query.filter_by(key = k).all()

	if not a:
		return False
	else:
		return True

@app.errorhandler(400)
def badRequestType():
	return {"status":"failed", "msg":"Bad request type"}, 400


@app.errorhandler(406)
def badApiKey():
	return {"status":"failed", "msg":"bad api key"}, 406


@app.route("/find-item", methods=["POST"])
def findItem():
	if request.method != "POST":	
		return badRequestType()		
		
	data = json.loads(request.data)
	if isValidKey(data['key']) == False:
		return badApiKey()

	#resp = hyvee.runQuery(data['searchTerm'], data['numResults'])		
	ids = bakers.getProductIds(data['searchTerm'], data['numResults'])
	#ids = hyvee.getProductIds(resp)
	#prods = hyvee.getProductData(ids)
	output = bakers.getProductInfo(ids)

	return output 

@app.route("/gen-api-key")
def query_test():
	k = generateAPIKey()
	a = ApiObject(k)
	db.session.add(a)
	db.session.commit()

	return {"status": "success", "msg": "key created", "key": k}

"""
	#ApiObject.query.all()
	a = ApiObject("test two")
	db.session.add(a)
	db.session.commit()
	return "successful write"
"""


if __name__ == "__main__":
	#db.create_all()
	app.run()



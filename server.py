#!/usr/bin/python3

from flask import Flask, request
from flask_cors import CORS
import requests
import hyvee_api as hyvee
import json


app = Flask(__name__)
CORS(app)

@app.errorhandler(400)
def badRequestType():
	return {"status":"failed", "msg":"Bad request type"}, 400


@app.route("/find-item", methods=["POST"])
def findItem():
	if request.method != "POST":	
		return badRequestType()		
		
	data = json.loads(request.data)
	resp = hyvee.runQuery(data['searchTerm'], data['numResults'])		
	ids = hyvee.getProductIds(resp)
	prods = hyvee.getProductData(ids)

	return hyvee.createJsonOutput(prods) 


if __name__ == "__main__":
	app.run()



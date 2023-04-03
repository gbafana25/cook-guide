#!/usr/bin/python3

from flask import Flask, request
from flask_cors import CORS
import requests
import hyvee_api as hyvee
import os
import pytesseract
import json
import shutil

pytesseract.tessearct_cmd = "tesseract"

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

def parseNutritionLabel(img):
	d = []
	d.append(img[2]+" "+img[3]+" "+img[4]+" "+img[5])
	for i in range(len(img)):
		img[i] = img[i].lower()
		if img[i] == "serving" and img[i+1] == "size":
			d.append("Serving size: "+img[i+2]+" "+img[i+3]+" "+img[i+4])
		elif img[i] == "calories":
			d.append("Calories: "+img[i+1])
		elif img[i] == "fiber":
			d.append(img[i]+" "+img[i+1])

	return d
	

@app.route("/nutrition", methods=["POST"])
def getNutritionFacts():
	if request.method != "POST":
		return badRequestType()
	
	data = json.loads(request.data)
	image_urls = data['urls']
	for im in image_urls:
		r = requests.get(im, stream=True)
		r.raw.decode_content = True

		# delete temp.jpg when finished

		with open("temp.jpg", "wb+") as temp_img:
			shutil.copyfileobj(r.raw, temp_img)

		
		# not all info from labels appears in array
		# image should also be displayed in frontend for now
		imgtext = pytesseract.image_to_string("temp.jpg")
		imgtext = imgtext.replace('\n', ' ').split(' ')	
		
		if imgtext[0] == "Nutrition" and imgtext[1] == "Facts":
			return parseNutritionLabel(imgtext)

	os.remove("temp.jpg")
	return {"status":"failed"}


if __name__ == "__main__":
	app.run()



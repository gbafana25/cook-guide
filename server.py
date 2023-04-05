#!/usr/bin/python3

from flask import Flask, request
from flask_cors import CORS
import requests
#import hyvee_api as hyvee
import bakers_api as bakers
import os
import pytesseract
import cv2
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
	#resp = hyvee.runQuery(data['searchTerm'], data['numResults'])		
	ids = bakers.getProductIds(data['searchTerm'], data['numResults'])
	#ids = hyvee.getProductIds(resp)
	#prods = hyvee.getProductData(ids)
	output = bakers.getProductInfo(ids)

	return output 

def parseNutritionLabel(img, start):
	d = []
	d.append(img[start+2]+" "+img[start+3]+" "+img[start+4]+" "+img[start+5])
	for i in range(start, len(img)):
		img[i] = img[i].lower()
		if img[i] == "serving" and img[i+1] == "size":
			d.append("Serving size: "+img[i+2]+" "+img[i+3]+" "+img[i+4])
		elif img[i] == "calories":
			d.append("Calories: "+img[i+1])
		elif img[i] == "fiber":
			d.append(img[i]+" "+img[i+1])

	return d
	
@app.route("/ingredients", methods=["POST"])
def getIngredients():
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
		start = imgtext.replace('\n', ' ').split(' ')
		#print(start)
		if start[0][:10].lower() == "ingredients" or start[0][:3].lower() == "made":
			return {"ingredients":imgtext} 

	os.remove("temp.jpg")
	return {"status":"failed", "msg":"no ingredients list found"}

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
		jpg = cv2.imread("temp.jpg")
		imgtext = pytesseract.image_to_string(jpg)
		imgtext = imgtext.replace('\n', ' ').split(' ')	
		
		#print(imgtext)
		for i in range(len(imgtext)):
			if imgtext[i].lower() == "nutrition" and imgtext[i+1].lower() == "facts":
				return parseNutritionLabel(imgtext, i)

	os.remove("temp.jpg")
	return {"status":"failed"}


if __name__ == "__main__":
	app.run()



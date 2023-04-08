from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import bakers_api as bakers
import json

# Create your views here.
@csrf_exempt
def findItem(request):
	if request.method != "POST":	
		return HttpResponse("fail")		
		
	data = json.loads(request.body.decode('utf-8'))
	"""
	if isValidKey(data['key']) == False:
		return HttpResponse("fail")
	"""

	ids = bakers.getProductIds(data['searchTerm'], data['numResults'])
	output = bakers.getProductInfo(ids)

	#return HttpResponse(json.dumps(output), content_type="application/json")
	return JsonResponse(output)

def isValidKey(k):
	#j = json.loads(request.data)

	a = ApiObject.query.filter_by(key = k).all()

	if not a:
		return False
	else:
		return True

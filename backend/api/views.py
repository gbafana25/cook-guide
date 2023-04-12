from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import secrets
import bakers_api as bakers
import json
from datetime import datetime

from .models import ApiKey
from .forms import SearchForm

KEY_LENGTH = 45

# Create your views here.
#@csrf_exempt
def results(key, term, num):	

	ids = bakers.getProductIds(term, num)
	output = bakers.getProductInfo(ids)

	#return HttpResponse(json.dumps(output), content_type="application/json")
	return output

def search(request):
	if request.method == "POST":
		seform = SearchForm(request.POST)
		if seform.is_valid():	
			
			# make this part less redundant, but works as intended now

			# if api key is not in a cookie, use the one in the form
			if 'apiKey' in request.COOKIES:
				if isValidKey(request.COOKIES['apiKey']) == False:
					return HttpResponse("fail")
				else:
					out = results(request.COOKIES['apiKey'], seform.cleaned_data['searchTerm'], seform.cleaned_data['numResults'])

					k = ApiKey.objects.get(key=request.COOKIES['apiKey'])
					k.current_search = out
					k.save()

					response = render(request, 'api/results.html', {"products": k.current_search['products'], "key":k.key})
	
					return response
			
			else:
				if isValidKey(seform.cleaned_data['apiKey']) == False:
					return HttpResponse("fail")
				else:

					out = results(seform.cleaned_data['apiKey'], seform.cleaned_data['searchTerm'], seform.cleaned_data['numResults'])

					k = ApiKey.objects.get(key=seform.cleaned_data['apiKey'])
					k.current_search = out
					k.save()

					response = render(request, 'api/results.html', {"products": k.current_search['products'], "key":k.key})

					if 'apiKey' not in request.COOKIES:
						now = datetime.now()
						future = datetime(now.year+1, now.month, now.day)
						response.set_cookie('apiKey', seform.cleaned_data['apiKey'], expires=future)
			
					return response 
	else:
		return render(request, "api/search.html", {})

	return render(request, "api/search.html", {})



def product_view(request, name):
	# change to product id (upc)
	key = request.COOKIES['apiKey']
	k = ApiKey.objects.get(key=key)
	p = {}
	url = ''
	for prod in k.current_search['products']:
		if prod['name'] == name:
			p = prod
	for u in p['urls']:
		if "large/front" in u:
			url = u		

	return render(request, "api/product-view.html", {"product": p, "url":url})	
def addProduct(request, name):
	key = request.COOKIES['apiKey']
	k = ApiKey.objects.get(key=key)
	# find name in current request, then add object to list
	#print(name)
	if k.item_list == None:
		k.item_list = {}

	if 'items' not in k.item_list:
		k.item_list['items'] = []

	for p in k.current_search['products']:
		if p['name'] == name:
			k.item_list['items'].append(p)
			k.save()
			return redirect('/cart')
			#return HttpResponse("success")


	k.save()
	return HttpResponse("fail")

def deleteProduct(request, name):	
	key = request.COOKIES['apiKey']
	k = ApiKey.objects.get(key=key)
	
	for p in range(len(k.item_list['items'])):
		if k.item_list['items'][p]['name'] == name:
			k.item_list['items'].pop(p)
			k.save()	
			#return HttpResponse("success")
			return redirect('/cart')


	k.save()
	return HttpResponse("fail")

def loadCart(request):
	key = request.COOKIES['apiKey']
	k = ApiKey.objects.get(key=key)

	# compare flag might not be necessary
	for i in k.item_list['items']:
		i['compare'] = False
	k.save()

	return render(request, 'api/cart.html', {'items':k.item_list['items']})

def compareItems(request):
	key = request.COOKIES['apiKey']
	k = ApiKey.objects.get(key=key)

	chosen = []
	cal_low = k.item_list['items'][0]['calories']
	price_low = k.item_list['items'][0]['price']

	for i in range(len(k.item_list['items'])):
		item = k.item_list['items'][i]
		if item['name'] in request.POST:
			if 'calories' in item:
				if item['calories'] < cal_low:
					cal_low = item['calories']
			if item['price'] < price_low:
				price_low = item['price']

			chosen.append(k.item_list['items'][i])


	return render(request, 'api/compare-view.html', {'items':chosen, 'cal_low':cal_low, 'price_low':price_low})


def isValidKey(k):
	try:
		obj = ApiKey.objects.get(key=k)
		obj.num_requests += 1
		obj.save()
		return True
	except:
		return False


def generateAPIKey(request):
	k = secrets.token_urlsafe(KEY_LENGTH)
	api_key = ApiKey.objects.create(key=k)
	api_key.save()

	return JsonResponse({"key": k})	



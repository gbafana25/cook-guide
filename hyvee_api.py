import requests
import json

base_url = "https://www.hy-vee.com/aisles-online"
	
# passes user-inputted string to first API request
def runQuery(term, num):
	f = open("search_query.json", "r")
	d = json.load(f) 
	d['variables']['input']['searchTerm'] = term
	d['variables']['input']['pageInfoInput']['pageSize'] = num 
	q_string = json.dumps(d, indent=4)
	
	response = makeRequest(q_string, "/api/graphql/two-legged/GetProductsAndFiltersFromElasticsearch")

	return response

# uses product ids from 1st request to get full product information
def getProductData(id_list):
	f = open("product_query.json", "r")
	d = json.load(f) 

	# number of items returned depends on length of whereIds
	# this is already limited in getQuery() 
	d['variables']['whereIds'] = id_list
		
	q_string = json.dumps(d, indent=4)

	response = makeRequest(q_string, "/api/graphql/two-legged/LoadSearchProductsForProductCardsQuery")
	return response


# request helper method
def makeRequest(json_data, endpoint):
	h = {"Content-Length":str(len(json_data)), "Content-Type":"application/json"}

	j = requests.post(base_url+endpoint, headers=h, data=json_data)
	return j.text

# creates new json object out of data
def createJsonOutput(output):
	j = json.loads(output)
	parsed_output = {
		"products": [],	
	}
	for i in range(len(j['data']['products']['products'])):
		item =  j['data']['products']['products'][i]
		prod = {
			'name': item['name'],
			'size': item['size'],
			'price': item['storeProduct']['price'],
			'priceMultiple': item['storeProduct']['priceMultiple'],
			'isOnSale': item['storeProduct']['onSale'],
			'primaryImage':'',
			'otherImages': [],
			
		}
		for im in item['item']['images']:
			if im['isPrimaryImage'] == True:
				prod['primaryImage'] = im['url']
			else:
				prod['otherImages'].append(im['url'])


		parsed_output['products'].append(prod)			

	return parsed_output

# prints final json object
def printOutput(output):
	j = json.loads(output)
	for i in range(len(j['products'])):
		item = j['products'][i]
		print(item['name'])
		print(item['size'])
		if item['isOnSale'] == True:
			print("On sale, " + str(item['priceMultiple']) + " for " + str(item['price']))
		else:
			print("Price: " + str(item['price']))
		
		print()

# grabs list of product IDs associated with search term
def getProductIds(search_data):
	j = json.loads(search_data)
	ids = []
	for i in range(len(j['data']['searchProductsResultV2']['searchProducts'])):
		item = j['data']['searchProductsResultV2']['searchProducts'][i]
		ids.append(item['productId'])
	return ids
	


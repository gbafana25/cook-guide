import requests
import json

base_url = "https://www.hy-vee.com/aisles-online"
	

def searchQuery(term):
	f = open("search_query.json", "r")
	d = json.load(f) 
	d['variables']['input']['searchTerm'] = term
	d['variables']['input']['pageInfoInput']['pageSize'] = 5 
	q_string = json.dumps(d, indent=4)
	
	response = makeRequest(q_string, "search_data.json")
	return response

def getProductData(id_list):
	f = open("product_query.json", "r")
	d = json.load(f) 

	d['variables']['whereIds'] = id_list
	
	
	q_string = json.dumps(d, indent=4)

	response = makeRequest(q_string, "product_output.json")
	return response

def makeRequest(json_data, outfile_name):
	h = {"Content-Length":str(len(json_data)), "Content-Type":"application/json"}

	j = requests.post(base_url+"/api/graphql/two-legged/LoadSearchProductsForProductCardsQuery", headers=h, data=json_data)
	#res = open(outfile_name, "w+")
	#res.write(j.text)
	return j.text

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
			
		}
		parsed_output['products'].append(prod)			

	return json.dumps(parsed_output)

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

def readPrelimSearch(search_data):
	j = json.loads(search_data)
	ids = []
	for i in range(len(j['data']['searchProductsResultV2']['searchProducts'])):
		item = j['data']['searchProductsResultV2']['searchProducts'][i]
		ids.append(item['productId'])
	return ids
	

if __name__ == "__main__":
	item = input("Enter an item to search: ")
	print()
	search_resp = searchQuery(item)
	prod_ids = readPrelimSearch(search_resp)
	out = getProductData(prod_ids)
	fmted = createJsonOutput(out)
	print(fmted)
	#printOutput(fmted)
	

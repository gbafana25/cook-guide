import requests
import json

base_url = "https://www.bakersplus.com/atlas/v1"

x_laf_obj = [{"fallbackFulfillment":"61500319","createdDate":1680651730116,"destination":{"locationId":"61500319"},"id":"8ba8856f-fae5-4b77-95d4-25f37700fed2","isCrossBanner":False,"modalityType":"PICKUP","source":"DEFAULT_MODALITY_ADDRESS","fulfillment":["61500319"],"isTrustedSource":False},{"fallbackDestination":"61500319","createdDate":1680651730114,"destination":{"address":{"postalCode":"68106"},"location":{"lat":41.24147797,"lng":-95.99941254}},"id":"9fc412fe-d979-4dec-af97-c27be4047a1b","fallbackFulfillment":"491DC001","modalityType":"SHIP","source":"SHIP_AUTOGEN","fulfillment":["491DC001","309DC309","310DC310","DSV00001","MKTPLACE"],"isTrustedSource":False}]

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

h = {"User-Agent": user_agent, "Accept":"*/*", "Host":"www.bakersplus.com", "x-laf-object":json.dumps(x_laf_obj)}

def getProductIds(query, num):
	#query = "rice"
	ids = []

	req = requests.get(base_url+"/search/v1/products-search?filter.query="+query+"&page.size="+str(num), headers=h)

	jdat = json.loads(req.text)

	for n in jdat['data']['productsSearch']:
		#print(n['upc'])
		ids.append(n['upc'])
	return ids

def parseProductData(raw):
	#print(raw)
	data = json.loads(raw)	
	parsed = []
	for item in data['data']['products']:
		prod = {}
		prod['name'] = item['item']['description']
		
		# REMINDER: also could include nfor, nforprice, unit price, price
		prod['price'] = item['price']['storePrices']['regular']['defaultDescription']
		try:
			#prod['nutrition'] = item['nutrition']
			prod['allergens'] = item['nutrition']['allergens']
			prod['ingredients'] = item['nutrition']['components'][0]['ingredients']
			prod['nutritionFacts'] = [] 
			for f in item['nutrition']['components'][0]['preparationStates'][0]['nutriFacts']:
				if f['name'].lower() == "calories":
					prod['calories'] = "Calories: "+f['value']
				else:
					prod['nutritionFacts'].append(f['name']+" "+f['value']+f['abbreviation'])
		except KeyError:
			prod['nutrition'] = "No nutrition info found"

		prod['categories'] = []
		for c in item['item']['categories']:
			if c['name'] not in prod['categories']:
				prod['categories'].append(c['name'])

		prod['urls'] = []
		for u in item['item']['images']:
			if "large/front" in u['url']:
				prod['urls'].append(u['url'])
		parsed.append(prod)

	#print(parsed)
	return {"products": parsed} 


def getProductInfo(ids):
	p = {"filter.gtin13s":[]}
	for i in ids:
		p["filter.gtin13s"].append(i)	

	req = requests.get(base_url+"/product/v2/products", headers=h, params=p)
	
	#print(req.text)
	return parseProductData(req.text)


"""
upcs = getProductIds("bread", 2)
parsed_data = getProductInfo(upcs)

for item in parsed_data:
	print(item['name'])
	print(item['price'])
	for i in item['categories']:
		print(i)
	#print(item['nutrition']['components'][0]['ingredients'])
	print()
"""

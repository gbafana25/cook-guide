import requests
import json

base_url = "https://www.hy-vee.com/aisles-online/"
	

def productjson():
	h = {"Content-Length":"3005", "Content-Type":"application/json"}
	f = open("query.json", "r")

	d = json.load(f) 
	j = requests.post("https://www.hy-vee.com/aisles-online/api/graphql/two-legged/LoadSearchProductsForProductCardsQuery", headers=h, data=json.dumps(d, indent=4))
	res = open("output.json", "w+")
	res.write(j.text)
	#print(j.text)

def readOutput():
	r = open("output.json")
	j = json.load(r)
	#print(j['data']['products']['products'])
	for i in range(5):#len(j['data']['products']['products']):
		item = j['data']['products']['products'][i]
		print(item['name'])
		if item['storeProduct']['onSale'] == True:
			print("On sale, " + str(item['storeProduct']['priceMultiple']) + " for " + str(item['storeProduct']['price']))
		else:
			print("Price: " + str(item['storeProduct']['price']))
		print()
	

if __name__ == "__main__":
	#productjson()
	readOutput()

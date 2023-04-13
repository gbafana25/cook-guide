# cook-guide

Product info is retrieved Baker's REST API (the same one used by the website).  Users can build a shopping cart and compare items.

## About

- `Apikey` object: holds randomly-generated string, number of requests made, results from last search, and the user's cart.
- The API key is returned from the `gen-api-key` endpoint, and can be entered in the search page, where it is then saved as a cookie.
- The search page returns a list of products and their prices.  Clicking on the item gives all of the product's information (nutrition info, allergens, category, picture, ingredients).
- Users can add the item to the cart, and then are redirected to `/cart`
- In the cart menu, users can select items to compare, change the quantity, and remove items

## About Baker's (Kroger) REST API

Both the Hyvee and Baker's APIs work in similar ways, in that they have a two-step process for obtaining product data.  First, the search query is sent to an endpoint that returns a list of product ids.  Then, a second request is made with the product ids, which then returns the data on all products.  The full article on this API's driver can be found [here](https://dev.to/gbafana25/undocumented-apis-in-websites-42g6)

## About Hy-Vee GraphQL API (not used anymore)

Two requests are required in order to get a list of potential products. Each GraphQL query is stored in a JSON format in the project's home directory.

1. Get product IDs from first endpoint, `/GetProductsAndFiltersFromElasticsearch`.  These IDs are then passed to the 2nd call.
2. product matches: returns basic product info (price, name, size, aisle/location, whether it's on sale, etc.) as well as images


## Testing/Development
- create a virtualenv and set it up: 
```bash	

python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

```
- run the server: `cd backend && python3 manage.py runserver`

## TODO:
- find way to export grocery list?

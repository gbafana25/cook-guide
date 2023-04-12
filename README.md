# cook-guide

Gets product info using Hy-Vee's "hidden" GraphQL api.  Final app will allow users to make a grocery list, budget out items, and possibly view nutrition info.   

Use Flask as backend to interact with store's API.  Use React on frontend (hopefully).

## Layout
- user does action to add item: search query is sent to Flask backend, which uses that to build GraphQL query for store's API
- top options from product search are returned, user can compare and choose one
- items' data is saved in current list, and also backed up to be included in future grocery lists
	- data from search querys can also be saved to reduce API requests (rate limits unknown)
- Reminder: can get rate limited if same request (search term is reused) is made multiple times. Changing the search term seems to immediately fix it.

## About Baker's (Kroger) REST API

Both the Hyvee and Baker's APIs work in similar ways, in that they have a two-step process for obtaining product data.  First, the search query is sent to an endpoint that returns a list of product ids.  Then, a second request is made with the product ids, which then returns the data on all products.  The full article on this API's driver can be found [here](https://dev.to/gbafana25/undocumented-apis-in-websites-42g6)

## About Hy-Vee GraphQL API (not used anymore)

Two requests are required in order to get a list of potential products. Each GraphQL query is stored in a JSON format in the project's home directory.

1. Get product IDs from first endpoint, `/GetProductsAndFiltersFromElasticsearch`.  These IDs are then passed to the 2nd call.
2. product matches: returns basic product info (price, name, size, aisle/location, whether it's on sale, etc.) as well as images


## Testing/Development
- run a mock http server (`python3 -m http.server`), since chromium doesn't allow cookies to be set by static html/js files

## TODO:

# cook-guide

Gets product info using Hy-Vee's "hidden" GraphQL api.  Final app will allow users to make a grocery list, budget out items, and possibly view nutrition info.   

Use Flask as backend to interact with store's API.  Use React on frontend (hopefully).

## Layout
- user does action to add item: search query is sent to Flask backend, which uses that to build GraphQL query for store's API
- top options from product search are returned, user can compare and choose one
- items' data is saved in current list, and also backed up to be included in future grocery lists
	- data from search querys can also be saved to reduce API requests (rate limits unknown)
- Reminder: can get rate limited if same request (search term is reused) is made multiple times. Changing the search term seems to immediately fix it.

## About Hy-Vee GraphQL API

Two requests are required in order to get a list of potential products. Each GraphQL query is stored in a JSON format in the project's home directory.

1. Get product IDs from first endpoint, `/GetProductsAndFiltersFromElasticsearch`.  These IDs are then passed to the 2nd call.
2. product matches: returns basic product info (price, name, size, aisle/location, whether it's on sale, etc.) as well as images

**Note: For rate limiting, find out if switching the user agent circumvents it.  If thiis would be used to deploy as a service, it would not be able to accept a high volume of requests exceeding that of a normal browser**

## Testing/Development
- run a mock http server (`python3 -m http.server`), since chromium doesn't allow cookies to be set by static html/js files

## TODO:
- fix weird image alignment in cart
- improve parsing of nutrition labels, add for ingredient labels (only for hyvee api, since baker's already provides info in text form)

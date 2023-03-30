# cook-guide

Gets product info using Hy-Vee's "hidden" GraphQL api.  Final app will allow users to make a grocery list, budget out items, and possibly view nutrition info.   

Use Flask as backend to interact with store's API.  Use React on frontend (hopefully).

## Layout
- user does action to add item: search query is sent to Flask backend, which uses that to build GraphQL query for store's API
- top options from product search are returned, user can compare and choose one
- items' data is saved in current list, and also backed up to be included in future grocery lists
	- data from search querys can also be saved to reduce API requests (rate limits unknown)

## About Hy-Vee GraphQL API
- product search: returns basic product info (price, name, size, aisle/location, whether it's on sale, etc.) as well as images

## TODO:
- modify graphql query so that it can be reused

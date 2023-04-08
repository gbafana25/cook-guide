function getKey() {
	let name = "apikey=";
	let decodedCookie = decodeURIComponent(document.cookie);
    	let ca = decodedCookie.split(';');
      	for(let i = 0; i <ca.length; i++) {
        	let c = ca[i];
	      	while (c.charAt(0) == ' ') {
	        	c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

function displayItems() {
	const full = new URL(window.location.toLocaleString()).searchParams;
	var k = getKey();
	const query = {"searchTerm":full.get('searchTerm'), "numResults":full.get('numResults'), "key":k};
	let a = document.getElementById('item-list');

	fetch("http://localhost:8000/find-item", {
		method: "POST",
		mode: "cors",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(query),
	}).then(function(resp) {
		return resp.json();
	}).then(function(dis) {
		console.log(dis);
		let list = document.querySelector("#basic-info").innerHTML;

		let data = {
			"products": dis.products,
		};

		let scr = Handlebars.compile(list);
		document.body.innerHTML = scr(data);
		//console.log(items);
		/*
		for(var i = 0; i < dis.length; i++) {
			var n = document.createElement('li');
			var addstr = dis[i].name+" "+dis[i].price+" "+dis[i].categories;
			n.appendChild(document.createTextNode(addstr));
			document.querySelector('ul').appendChild(n);
		}
		//let e = a.createElement('li');
		*/

	});
		
}


displayItems();



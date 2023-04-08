function getKey() {
	let name = "apikey=";
	let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function displayItems() {
	const full = new URL(window.location.toLocaleString()).searchParams;
	//console.log(full.get('searchTerm'));
	//var k = getKey();
	//console.log(k);
	const query = {"searchTerm":full.get('searchTerm'), "numResults":full.get('numResults'), "key":full.get('key')};
	let a = document.getElementById('item-list');

	fetch("http://localhost:5000/find-item", {
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
			"products": dis,
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



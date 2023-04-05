

function displayItems() {
	const query = {"searchTerm":"hummus", "numResults":10};
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



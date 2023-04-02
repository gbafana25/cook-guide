

function displayItems() {
	const query = {"searchTerm":"bread", "numResults":4};
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
		//console.log(items);
		for(var i = 0; i < dis.length; i++) {
			var n = document.createElement('li');
			n.appendChild(document.createTextNode(dis[i].name));
			document.querySelector('ul').appendChild(n);
		}
		//let e = a.createElement('li');

	});
		
}


displayItems();



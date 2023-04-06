document.addEventListener("DOMContentLoaded", () => {
	const full = new URL(window.location.toLocaleString()).searchParams;
	let view = document.querySelector("#product").innerHTML;
	let data = {
		"name": full.get('name'),
		"price": full.get('price'),
		"categories": full.get('cat'),
		"allergens": full.get('allergens'),
		"image": full.get('image'),
	};

	let scr = Handlebars.compile(view);
	document.body.innerHTML = scr(data);
});

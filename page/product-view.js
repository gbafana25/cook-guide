document.addEventListener("DOMContentLoaded", () => {
	const full = new URL(window.location.toLocaleString()).searchParams;
	let view = document.querySelector("#product").innerHTML;
	const narray = full.get('facts').split(',');
	let data = {
		"name": full.get('name'),
		"price": full.get('price'),
		"categories": full.get('cat'),
		"allergens": full.get('allergens'),
		"image": full.get('image'),
		"ingredients": full.get('ingredients'),
		"nutri_facts": narray,
	};

	let scr = Handlebars.compile(view);
	document.body.innerHTML = scr(data);
});

//const b = document.getElementById('keybtn');
var k;
window.onload = function() {
	k = document.getElementById('key');
};


//b.addEventListener('click', saveKey);

function saveKey() {
	var c = "apikey="+k.value+"";
	//console.log(`${document.cookie}`);
	//console.log(c);
	document.cookie = c;
	console.log(document.cookie);

}

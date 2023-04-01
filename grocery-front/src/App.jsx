import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";

import "./index.css";

const App = () => {
	let j = {searchTerm:"bread", numResults:3};
	let jstr = JSON.stringify(j);
	const [products, setList] = useState([]);

	useEffect(() => {
		prods();
		//console.log(products);
	}, []);

	const prods = async () => {
		const res = await fetch("http://localhost:5000/find-item", {
			method: "POST",
			mode: "cors",
			headers: {
				"Content-Type":"application/json",
			},
			body: jstr,
		});
		setList(await res.json());
		//console.log(await res.json());
	}

	

  return (

  <div className="container">
  {products.map((p) => (
  	<>
  	<p>{p.name} {p.size}</p>
	<p>{p.price}</p>
	</>

  ))}
  </div>

  );

};
ReactDOM.render(<App />, document.getElementById("app"));

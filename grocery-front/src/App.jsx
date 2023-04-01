import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";

import "./index.css";

async function getData() {
	let j = {searchTerm:"bread", numResults:3};
	let jstr = JSON.stringify(j);
	const res = await fetch("http://localhost:5000/find-item", {
			method: "POST",
			//mode: "cors",
			headers: {
				"Content-Type": "application/json",
			},
			cache: "no-cache",
			body: jstr,
		
		});
	return res.json();
}

const App = () => {
	const [prod, d] = useState([]);

	useEffect(() => {
		getData();
	}, []);

  return (

  <div className="container">
    <ul>
    { prod.map((p) => <li key={p}>{p}</li>) }
    </ul>
  </div>

  );

};
ReactDOM.render(<App />, document.getElementById("app"));

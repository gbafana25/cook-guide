import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";

import './search.css';

class Search extends React.Component {
	//const j = {searchTerm:"granola bars", numResults:3};
	//let jstr = JSON.stringify(j);
	const [products, setList] = useState([]);

	const res = fetch("http://localhost:5000/find-item", {
			method: "POST",
			mode: "cors",
			headers: {
				"Content-Type":"application/json",
			},
			body: JSON.stringify({searchTerm:"granola bars", numResults:3}),
		});
	
	setList(res.json());

	render() {
  		return <p>test</p>;
	}

}

export default Search;

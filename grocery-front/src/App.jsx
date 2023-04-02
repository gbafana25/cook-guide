import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import Search from './search.jsx';

import "./index.css";

const App = () => {	

  return (

  <div className="container">
 	<Search /> 
  </div>

  );

};
ReactDOM.render(<App />, document.getElementById("app"));

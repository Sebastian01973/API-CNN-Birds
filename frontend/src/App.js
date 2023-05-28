import React, { Component } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ImageUpload from "./components/ImageUpload";
import Home from "./Pages/Home";
import Page404 from "./Pages/Page404";

import Navbar from "./components/Navbar";

import "./App.css";

class App extends Component {
  render() {
    return (
      <Router>
        <div className="bg-dark text-light">
          <Navbar />
          <div className="container p-4">
            <Routes>
              <Route path="/" element={<Home />} exact />
              <Route path="/upload" element={<ImageUpload />} />
              <Route path="*" element={<Page404 />} />
            </Routes>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;

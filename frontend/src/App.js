import React, { Component } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ImageUpload from "./components/ImageUpload";
import Home from "./Pages/Home";
import Page404 from "./Pages/Page404";

import Navbar from "./Pages/Navbar";

import "./App.css";

class App extends Component {
  render() {
    
    const galleryImages = [
      {
        img: "/img/1.jpg",
      },
      {
        img: "/img/2.jpg",
      },
      {
        img: "/img/3.jpg",
      },
      {
        img: "/img/4.jpg",
      },
      {
        img: "/img/5.jpg",
      },
      {
        img: "/img/6.jpg",
      },
      {
        img: "/img/7.jpg",
      },
      {
        img: "/img/8.jpg",
      },
      {
        img: "/img/9.jpg",
      },
      {
        img: "/img/10.jpg",
      },
    ];
    return (
      <Router>
        <div className="bg-dark text-light">
          <Navbar />
          <div className="container p-4">
            <Routes>
              <Route
                path="/"
                element={<Home galleryImages={galleryImages} />}
                exact
              />
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

import React, { useState } from "react";
import axios from "axios";

import PredictionModel from "./PredictionModel";

const ImageUpload = () => {
  const [prediction, setPrediction] = useState("");
  const [image, setImage] = useState(null);
  const [uploadPercentage, setUploadPercentage] = useState(0);
  const [loading, setLoading] = useState(false);

  const [isData, setIsData] = useState(false);

  const handleChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    //Envia al backend la foto
    const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress(progressEvent) {
        const { loaded, total } = progressEvent;
        let percent = parseInt((loaded * 100) / total);
        setUploadPercentage(percent);
      },
    });

    setLoading(false);
    setUploadPercentage(0);

    setPrediction(res.data);

    setIsData(true);
  };

  return (
    <div className="container">
      <div className="col-md-4 offset-md-4">
        {loading && (
          <div className="progress rounded-0">
            <div
              className="progress-bar progress-bar-striped bg-success"
              role="progressbar"
              style={{ width: `${uploadPercentage}%` }}
            >
              {uploadPercentage}%
            </div>
          </div>
        )}
        <div className="card bg-dark text-light rounded-0 p-4">
          <div className="card-body">
            <h3>Upload an Image</h3>
            <p>Upload an image to classify the bird species</p>
            <form onSubmit={handleSubmit}>
              <input
                type="file"
                className="form-control mb-3"
                accept=".png, .jpg, .jpeg"
                onChange={handleChange}
              />
              <div className="my-3">
                <button className="btn btn-success rounded-0 w-100">
                  Upload
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div className="container">
      {/* Validar que se hace cuando no se sube una imagen */}
        {isData && <PredictionModel imageURL={image} prediction={prediction} />}  
      </div>
    </div>
  );
};

export default ImageUpload;

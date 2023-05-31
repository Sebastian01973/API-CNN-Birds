import React from "react";

const PredictionModel = (props) => {

  const { imageURL, prediction } = props;

  // console.log("A ver que pasa: ",imageURL);

  // Esperar que se haga el submir para actualizar los props

  const verifyImage = (image) => {
    if (image === undefined) {
      return ""
    }
    return URL.createObjectURL(image)
  }

  return (
    
    <div className="row">
      <div className="col-md-6 offset-md-4">
        <div className="card bg-dark">
          <img
            src={verifyImage(imageURL)}
            alt={prediction}
            className="card-img-top"
          />
          <div className="card-body">
            <h3 className="">{prediction}</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionModel;

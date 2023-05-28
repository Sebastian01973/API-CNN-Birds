import React from "react";

const PredictionModel = (props) => {

  const { imageURL, prediction } = props;

  console.log("En prediction: ",prediction, imageURL);
  // console.log("Image: ",URL.createObjectURL(imageURL));

  return (
    <div className="row">
      <div className="col-md-4 offset-md-4">
        <div className="card bg-dark">
          <img
            src={URL.createObjectURL(imageURL)}
            alt={prediction}
            className="card-img-top"
          />
          <div className="card-body">
            <h3 className="">{prediction.result}</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionModel;

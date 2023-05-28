import React, {useState} from 'react';
import axios from 'axios';

const ImageUpload = () => {

  const [image, setImage] = useState(null);

  const handleChange = (e) => {
    console.log(e.target.files[0]);
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', image);

    //Envia al backend la foto uwu
    const res = await axios.post('http://127.0.0.1:5000/upload', formData);

    console.log(res);
  };
  
  return (
    <div className='col-md-4 offset-md-4'>
      <div className='card bg-dark text-light rounded-0 p-4'>
        <div className='card-body'>
          <h3>Upload an Image</h3>
          <p>Upload an image to classify the bird species</p>
          <form onSubmit={handleSubmit}>
            <input type='file' className='form-control mb-3' 
              onChange={handleChange}
            />
            <div className='my-3'>
              <button className='btn btn-success rounded-0 w-100'>
                Upload
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;
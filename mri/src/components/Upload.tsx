import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// import UploadImage from './UploadImage';
// import DisplayImage from './DisplayImage';

const UploadFile: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const navigate = useNavigate(); //for navigation

const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0] || null;

  if (file && !['image/jpeg', 'image/png'].includes(file.type)) {
    alert('Only JPG or PNG images are allowed.');
    event.target.value = ''; // reset input
    setSelectedFile(null);
    return;
  }

  setSelectedFile(file);
};

  const handleUpload = () => {
    if (!selectedFile) {
      alert("No file selected");
      return;
    }

    // Simulate upload (temporary - FILE UPLOAD STUFF GOES HERE)
    console.log("Uploading file:", selectedFile.name);

    // Navigate to the analysis page, only when a file is uploaded
  navigate('/analysis', {
    state: {
      imageURL: selectedFile ? URL.createObjectURL(selectedFile) : null
    }
  });
};

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Upload File</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {selectedFile && <p>Selected File: {selectedFile.name}</p>}
      <button onClick={handleUpload} disabled={!selectedFile} className='main bg-orange-500/50 text-orange-800 px-4 py-2'>
        Upload
      </button>
    </div>
  );
};

export default UploadFile;

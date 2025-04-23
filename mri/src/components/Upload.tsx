import React, { useState } from 'react';

const UploadFile: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert("No file selected");
      return;
    }

    // For now, just logging. You could send it to a server here.
    console.log("Uploading file:", selectedFile.name);
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Upload File</h2>
      <input type="file" onChange={handleFileChange} />
      {selectedFile && <p>Selected File: {selectedFile.name}</p>}
      <button onClick={handleUpload} disabled={!selectedFile}>
        Upload
      </button>
    </div>
  );
};

export default UploadFile;

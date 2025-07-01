import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
// import UploadImage from './UploadImage';
// import DisplayImage from './DisplayImage';

const UploadFile: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const navigate = useNavigate(); //for navigation
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false); // for drag visual feedback

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

  // Trigger hidden file input
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  // Drag and drop handlers
  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);

    const file = event.dataTransfer.files?.[0] || null;

    if (file && !['image/jpeg', 'image/png'].includes(file.type)) {
      alert('Only JPG or PNG images are allowed.');
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  return (
    <div style={{ padding: "1rem" }}>

      <div className=" flex flex-1 justify-center py-5">
        <div className="layout-content-container flex flex-col py-5 flex-1">
          <h2 className=" tracking-light text-[28px] font-bold leading-tight px-4 text-center pb-3 pt-5">Upload Your File</h2>
          <p className=" text-base font-normal leading-normal pb-10 pt-1 px-4 text-center">
            Drag and drop a file here, or click to select a file from your computer. Supported formats: JPG, PNG.
          </p>

          {/* select file */}
          <div className="flex flex-col">

            <button onClick={handleUploadClick}>
              <div
                className={`flex flex-col items-center gap-6 rounded-lg border-2 px-6 py-14 
                  ${isDragging ? 'border-orange-500 bg-orange-100' : 'border-dashed border-[#A8A8A8]'}`
                }
                onDragOver={handleDragOver}
                onDragEnter={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <p className="text-lg font-bold leading-tight tracking-[-0.015em] max-w-[480px] text-center">Drag and drop your file here</p>
                <p className="text-sm font-normal leading-normal max-w-[480px] text-center">Or click to browse</p>
                {selectedFile && <p>Selected File: {selectedFile.name}</p>}
              </div>
            </button>
          </div>

          {/* Upload file */}
          <button onClick={handleUpload} disabled={!selectedFile} className='main bg-orange-500/50 text-orange-800 p-3 mb-100 mt-4'>
            Upload
          </button>
        </div>
      </div>

      {/* Hidden File Input */}
      <input
        type="file"
        accept="image/jpeg, image/png"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />

    </div>
  );
};

export default UploadFile;

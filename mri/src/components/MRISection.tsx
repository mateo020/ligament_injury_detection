import { useLocation } from 'react-router-dom';
import React, { useState, useRef } from 'react';

function MRISection() {
    const location = useLocation();
    const initialImageURL = (location.state as { imageURL: string })?.imageURL;
    const [localImage, setLocalImage] = useState<string | null>(initialImageURL || null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Handle file selection
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];

        if (file && !['image/jpeg', 'image/png'].includes(file.type)) {
            alert('Only JPG or PNG images are allowed.');
            event.target.value = '';
            return;
        }

        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setLocalImage(imageUrl);
        }
    };

    // Trigger hidden file input
    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    return (
        <section className="bg-gray-50 w-1/2 flex justify-center rounded-2xl relative">
            <div className="flex flex-col items-center w-full relative">

                {/* Image Bubble */}
                <div className="pt-5 flex items-center gap-2 absolute left-4 top-2">
                    <div className="bg-orange-500/50 py-1 px-3 flex justify-center items-center rounded-lg">
                        <span className="pr-1 text-orange-800 font-bold">Image</span>
                        <svg className="fill-orange-800" xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 -960 960 960"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120zm0-80h560v-560H200zm40-80h480L570-480 450-320l-90-120zm-40 80v-560z"/></svg>
                    </div>
                </div>

                {/* Legend */}
                <div className="rounded-lg border border-orange-500 absolute left-4 top-20 p-1 pr-4">
                    ACL Tear
                    <span className="bg-orange-500 w-15 h-2 inline-block ml-2"></span>
                </div>

                {/* ACL Tear MRI Image */}
                {localImage ? (
                    <img src={localImage} alt="Uploaded" className="pl-35 pt-24 md:pt-12 h-[80%] w-[80%]" />
                ) : (
                    <p className="pt-24">No image found.</p>
                )}

                {/* TODO: add functionality to the buttons */}
                {/* Buttons */}
                <div className="mt-6 mb-4 grid grid-cols-3 gap-2 w-full max-w-md px-4">
                    <button
                        onClick={handleUploadClick}
                        className="main bg-orange-500/50 text-orange-800 px-4 py-2 rounded-md"
                    >
                        Upload X-Ray
                    </button>
                    {/* <button className="main bg-orange-500/50 text-orange-800 px-4 py-2 rounded-md">Upload DICOM</button> */}
                    <button className="main bg-orange-500/50 text-orange-800 px-4 py-2 rounded-md">Clear Chat</button>
                    <button className="main bg-orange-500/50 text-orange-800 px-4 py-2 rounded-md">New Thread</button>
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
        </section>
    );
}

export default MRISection;

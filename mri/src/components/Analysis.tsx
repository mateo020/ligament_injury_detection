// import { useEffect } from 'react';

function Analysis() {
//   useEffect(() => {
//     // Disable scrolling
//     document.body.style.overflow = 'hidden';

//     // Optional cleanup on unmount
//     return () => {
//       document.body.style.overflow = 'auto';
//     };
//   }, []);

    return (
        <>
            {/* Title Text */}
            <header className="absolute top-4 left-8 font-bold text-4xl z-50 m-0 p-0">
                ACL Ligament Helper
            </header>

            {/* main section */}
            <main className="w-screen flex">
                {/* MRI Image Section */}
                <section className=" bg-gray-50 h-9/10 w-1/2 flex justify-center rounded-2xl absolute top-20 left-20">
                    <div className="flex flex-col items-center">
                    
                        {/* Image Bubble */}
                        <div className="pt-5 flex items-center gap-2 absolute left-4">
                            <div className="bg-orange-500/50 py-1 px-3 flex justify-center items-center rounded-lg">
                                <span className="pr-1 text-orange-800 font-bold">Image</span>
                                <svg className="fill-orange-800" xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 -960 960 960"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120zm0-80h560v-560H200zm40-80h480L570-480 450-320l-90-120zm-40 80v-560z"/></svg>

                            </div>
                        </div>

                        {/* Legend */}
                        <div className="rounded-lg border border-orange-500 absolute left-4 top-2/10 p-1 pr-4">
                            ACL Tear
                            <span className="bg-red-500 w-15 h-2 inline-block ml-2"></span>
                        </div>

                        {/* ACL Tear MRI Image */}
                        <img 
                            // TODO: change this image to uploaded image
                            src="https://www.hss.edu/images/articles/acl-tear.jpg"
                            alt="bones"
                            className="pt-12 h-[85%] w-[76%] absolute right-12"
                        /> 

                        {/* TODO: add functionality to the buttons */}
                        {/* Buttons */}
                        <div className="absolute bottom-4 grid grid-cols-2 gap-2 w-150">
                            <button className="">Upload X-Ray</button>
                            <button className="">Upload DICOM</button>
                            <button className="">Clear Chat</button>
                            <button className="">New Thread</button>
                        </div>
                    </div>

                </section>

                {/* chat section */}
                <aside className="bg-gray-50 h-9/10 w-4/10 absolute top-20 left-262 justify-center rounded-2xl ml-5">
                    {/* chat bubble */}
                    <div className="pt-5 flex justify-center items-center gap-2 absolute left-4">
                        <div className="bg-orange-500/50 py-1 px-3 flex justify-center items-center rounded-lg ">
                            <span className="pr-1 text-orange-800 font-bold">Chat</span>
                            <svg className="fill-orange-800" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 -960 960 960">
                            <path d="M80-80v-720q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H240zm126-240h594v-480H160v525zm-46 0v-480z"/>
                            </svg>
                        </div>
                    </div>

                    {/* TODO: complete the chat section */}
                </aside>
            </main>
        </>
    );
}

export default Analysis;

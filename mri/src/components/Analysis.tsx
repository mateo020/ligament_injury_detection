// import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Analysis() {  
    const navigate = useNavigate(); //for navigation  
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
            <header className="absolute top-4 left-8 font-bold text-4xl z-50 m-0 p-0 ">
                {/* <button 
                    className=" hover:animate-pulse"
                    onClick={() => navigate('/')}
                >
                    ACL Ligament Helper
                </button> */}


                <button 
                onClick={() => navigate('/')}
                className="group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md px-6 font-medium duration-500">
                    <div className="translate-x-0 opacity-100 transition group-hover:-translate-x-[150%] group-hover:opacity-0">
                        ACL Ligament Helper
                    </div>
                    <div className="absolute translate-x-[150%] opacity-0 transition group-hover:translate-x-0 group-hover:opacity-100">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-13 w-14">
                            <path d="M2.25 12L11.2045 3.04549C11.6438 2.60615 12.3562 2.60615 12.7955 3.04549L21.75 12M4.5 9.75V19.875C4.5 20.4963 5.00368 21 5.625 21H9.75V16.125C9.75 15.5037 10.2537 15 10.875 15H13.125C13.7463 15 14.25 15.5037 14.25 16.125V21H18.375C18.9963 21 19.5 20.4963 19.5 19.875V9.75M8.25 21H16.5" stroke="#0F172A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                            </path>
                        </svg>
                    </div>
                </button>
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
                            <span className="bg-orange-500 w-15 h-2 inline-block ml-2"></span>
                        </div>

                        {/* ACL Tear MRI Image */}
                        <img 
                            // TODO: change this image to uploaded image
                            src="https://upload.orthobullets.com/topic/3008/images/discon.jpg"
                            alt="bones"
                            className="pt-12 h-[85%] w-[76%] absolute right-12"
                        /> 

                        {/* TODO: add functionality to the buttons */}
                        {/* Buttons */}
                        <div className="absolute bottom-4 grid grid-cols-2 gap-2 w-150">
                            <button className="main bg-orange-500/50 text-orange-800 px-4 py-2">Upload X-Ray</button>
                            <button className="main bg-orange-500/50 text-orange-800 px-4 py-2">Upload DICOM</button>
                            <button className="main bg-orange-500/50 text-orange-800 px-4 py-2">Clear Chat</button>
                            <button className="main bg-orange-500/50 text-orange-800 px-4 py-2">New Thread</button>
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

                    {/* TODO: complete the chat section - needs backend*/}
                </aside>
            </main>
        </>
    );
}

export default Analysis;

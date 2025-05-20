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
            <header className="absolute top-4 left-8 font-bold text-4xl z-50 m-0 p-0">
                ACL Ligament Helper
            </header>

            <main className="w-screen flex">
                <section className=" bg-gray-50 h-9/10 w-1/2 flex justify-center rounded-2xl absolute top-20 left-20">
                    <div className="flex flex-col items-center">
                    
                        {/* TODO : make it look purdy */}
                        <div className="pt-5 flex items-center gap-2">
                                <span>Image</span>
                                <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        fill-rule="evenodd"
                                        clip-rule="evenodd"
                                        d="M2.5 1H12.5C13.3284 1 14 1.67157 14 2.5V12.5C14 13.3284 13.3284 14 12.5 14H2.5C1.67157 14 1 13.3284 1 12.5V2.5C1 1.67157 1.67157 1 2.5 1ZM2.5 2C2.22386 2 2 2.22386 2 2.5V8.3636L3.6818 6.6818C3.76809 6.59551 3.88572 6.54797 4.00774 6.55007C4.12975 6.55216 4.24568 6.60372 4.32895 6.69293L7.87355 10.4901L10.6818 7.6818C10.8575 7.50607 11.1425 7.50607 11.3182 7.6818L13 9.3636V2.5C13 2.22386 12.7761 2 12.5 2H2.5ZM2 12.5V9.6364L3.98887 7.64753L7.5311 11.4421L8.94113 13H2.5C2.22386 13 2 12.7761 2 12.5ZM12.5 13H10.155L8.48336 11.153L11 8.6364L13 10.6364V12.5C13 12.7761 12.7761 13 12.5 13ZM6.64922 5.5C6.64922 5.03013 7.03013 4.64922 7.5 4.64922C7.96987 4.64922 8.35078 5.03013 8.35078 5.5C8.35078 5.96987 7.96987 6.35078 7.5 6.35078C7.03013 6.35078 6.64922 5.96987 6.64922 5.5ZM7.5 3.74922C6.53307 3.74922 5.74922 4.53307 5.74922 5.5C5.74922 6.46693 6.53307 7.25078 7.5 7.25078C8.46693 7.25078 9.25078 6.46693 9.25078 5.5C9.25078 4.53307 8.46693 3.74922 7.5 3.74922Z"
                                        fill="currentColor"
                                    />
                                </svg>
                        </div>

                        <div className="rounded-lg border border-orange-500 absolute left-4 top-2/10 p-1 pr-4">
                            ACL Tear
                            <span className="bg-red-500 w-15 h-2 inline-block ml-2"></span>
                        </div>


                        <img 
                            // TODO: change this image to uploaded image
                            src="https://www.hss.edu/images/articles/acl-tear.jpg"
                            alt="bones"
                            className="pt-12 h-[85%] w-[76%] absolute right-12"
                        /> 

                        {/* TODO: add functionality to the buttons */}
                        <div className="absolute bottom-4 grid grid-cols-2 gap-2 w-150">
                            <button className="">Upload X-Ray</button>
                            <button className="">Upload DICOM</button>
                            <button className="">Clear Chat</button>
                            <button className="">New Thread</button>
                        </div>
                    
                    
                    </div>

                </section>

                <aside className="bg-gray-50 h-9/10 w-4/10 absolute top-20 left-262 justify-center rounded-2xl ml-5">
                    {/* TODO: make it look purdy */}
                    <div className="pt-5 flex justify-center items-center gap-2 w-full">
                        <span>Chat</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 -960 960 960">
                        <path d="M80-80v-720q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H240zm126-240h594v-480H160v525zm-46 0v-480z"/>
                        </svg>
                    </div>

                    {/* TODO: complete the chat section */}
                </aside>
            </main>
        </>
    );
}

export default Analysis;

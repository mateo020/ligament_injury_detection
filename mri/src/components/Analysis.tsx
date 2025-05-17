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
                    {/* IDK why this div bellow makes everything nicely aligned */}
                    <div>
                    
                    {/* TODO : change this to a little icon */}
                    <div className="pt-5">Image</div>

                    {/* TODO : add the buttons on the bottom and the labels on the left (ask mateo if wewill have the labels) */}
                   
                    <img 
                        // TODO: change this image to uploaded image
                        src="https://www.hss.edu/images/articles/acl-tear.jpg"
                        alt="bones"
                        className="pt-5 h-9/10 w-7/10 absolute right-8"
                    /> 
                    
                    </div>

                </section>

                <aside className="bg-gray-50 h-9/10 w-4/10 absolute top-20 left-262 justify-center rounded-2xl ml-5">
                    {/* TODO : change this to a little icon */}
                    <div className="pt-5">Chat</div> 
                </aside>
            </main>
        </>
    );
}

export default Analysis;

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
                
                {/* TODO make the divs wider prolly shorter too and a 50/50 size split - just make it like the new image */}
                <section className=" bg-gray-50 h-9/10 w-1/2 flex justify-center rounded-2xl absolute top-20 left-20">
                    {/* IDK why this div bellow makes everything nicely aligned */}
                    <div>
                    
                    <div className="pt-5">Deep Clinical Search</div>
                   
                    <img 
                        // TODO: change this image to uploaded image
                        src="https://www.hss.edu/images/articles/acl-tear.jpg"
                        alt="bones"
                        className=" pt-15"
                    /> 
                    
                    </div>

                </section>

                <aside className="bg-gray-50 h-9/10 w-4/10 absolute top-20 left-262 justify-center rounded-2xl ml-5">
                    <div className="pt-5">Explain My Scan</div> 
                </aside>
            </main>
        </>
    );
}

export default Analysis;

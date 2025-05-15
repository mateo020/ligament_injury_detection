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
        <div>
            <div className="absolute top-4 left-8 font-bold text-4xl z-50 m-0 p-0">
                ACL Ligament Helper
            </div>

            <div className="flex mt-15">
                
                {/* TODO make the divs wider and a 50/50 size split */}
                <div className="relative">
                    <img 
                        // change this image to uploaded image
                        src="https://www.hss.edu/images/articles/acl-tear.jpg"
                        alt="bones"
                        className="w-[3000px] h-[900px]"
                    />
                    
                    <div className="bg-white/75 h-[250px] w-2xl flex justify-center rounded-t-2xl">
                        <div className="pt-5">Deep Clinical Search</div>
                    </div>
                </div>

                <div className="bg-gray-100 w-[2000px] h-auto flex justify-center">
                    <div className="pt-5">Explain My Scan</div> 
                </div>
            </div>
        </div>
    );
}

export default Analysis;

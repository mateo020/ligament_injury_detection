import { useEffect } from 'react';

function Analysis() {
  useEffect(() => {
    // Disable scrolling
    document.body.style.overflow = 'hidden';

    // Optional cleanup on unmount
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, []);
  
    return (

        <div className="flex ">
            <div className="relative">
                <img 
                    // change this image to uploaded image
                    src="https://www.hss.edu/images/articles/acl-tear.jpg"
                    alt="bones"
                    className="w-[3000px] h-[900px]"
                />
                {/* Temporyary Blue, just to show the boundary
                    TODO: overlap with the bone pic (prolly z-axis)
                */}
                <div className="absolute bottom-0 left-7 bg-white/75 h-[250px] w-2xl flex justify-center rounded-t-2xl z-40">
                    <div className="pt-5">Deep Clinical Search</div>
                </div>
            </div>

            {/* Temporyary Red, just to show the boundary */}
            <div className="bg-red-500 w-[2000px] h-auto flex justify-center">
                <div className="pt-5">Explain My Scan</div>
            
                
                
            </div>
        </div>
    );
}

export default Analysis;

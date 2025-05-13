function Analysis() {
    return (
        <div className="flex">
            <div>
                <img 
                    src="https://www.hss.edu/images/articles/acl-tear.jpg"
                    alt="bones"
                    className="w-[1000px] h-auto"
                />
                {/* Temporyary Blue, just to show the boundary
                    TODO: rounded border
                    TODO: overlap with the bone pic (prolly z-axis)
                */}
                <div className="bg-blue-500 h-[250px] flex justify-center">
                    Deep Clinical Search
                </div>
            </div>

            {/* Temporyary Red, just to show the boundary */}
            <div className="bg-red-500 w-[1000px] flex justify-center">
                <div className="pt-5">Explain My Scan</div>
            
                
                
            </div>
        </div>
    );
}

export default Analysis;

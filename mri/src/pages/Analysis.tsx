// import { useEffect } from 'react'; 
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import MRISection from '../components/MRISection';
import ChatSection from '../components/ChatSection';

function Analysis() {  
    const navigate = useNavigate(); //for navigation 
    
    // useEffect(() => {
    //   // Disable scrolling
    //   document.body.style.overflow = 'hidden';

    //   // Optional cleanup on unmount
    //   return () => {
    //     document.body.style.overflow = 'auto';
    //   };
    // }, []);

    return (
        <>
            {/* Title Text */}
            <Header navigate={navigate} />

            {/* main section */}
            <main className="w-screen flex flex-col md:flex-row md:items-start md:justify-start pt-15 gap-4">
                <MRISection />
                <ChatSection />
            </main>
        </>
    );
}

export default Analysis;

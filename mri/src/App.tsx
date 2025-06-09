// import { useState } from 'react'
import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import Upload from "./components/Upload";
import Analysis from "./pages/Analysis";
import './App.css'


function Home(){
  return(
    <>
      <div className="columns-2">
        <h1 className='pb-5 pt-35'>ACL Ligament Helper</h1>
        <p className='pb-5'>Classify and detect types of ACL tears in MRI images with our algorythms</p>
        <Link to="/upload">
          <button className='main bg-orange-500/50 text-orange-800 px-4 py-2'>
            Get Started
          </button>
        </Link>
        <img src="https://upload.orthobullets.com/topic/3008/images/discon.jpg" alt="bones"
            width="500" 
            height="500" />
      </div>
    </>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/analysis" element={<Analysis />} />
      </Routes>
    </Router>
  )
}

export default App

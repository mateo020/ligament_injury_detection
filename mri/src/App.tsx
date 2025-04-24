// import { useState } from 'react'
import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import Upload from "./components/Upload";
import './App.css'


function Home(){
  return(
    <>
    <div className="columns-2">
      <h1 className='pb-5'>ACL Ligament Helper</h1>
      <p className='pb-5'>Classify and detect types of ACL tears in MRI images with our algorythms</p>
      <Link to="/upload">
        <button className='text-white'>
          Get Started
        </button>
      </Link>
      <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTr_mGmSutVv2ynXuPwalU_8QOGiOCqoMOQzA&s" alt="bones"
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
        \
      </Routes>
    </Router>
  )
}

export default App

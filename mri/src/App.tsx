// import { useState } from 'react'
import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import Upload from "./components/Upload";
import './App.css'


function Home(){
  return(
    <>
      <h1>ACL Ligament Helper</h1>
      <Link to="/upload">
        <button>
          Get Started
        </button>
      </Link>
      
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

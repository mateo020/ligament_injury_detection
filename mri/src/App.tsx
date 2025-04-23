import { useState } from 'react'
import reactLogo from './assets/react.svg'
import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import Upload from "./components/Upload";
import viteLogo from '/vite.svg'
import './App.css'


function Home(){
  return(
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <Link to="/upload">
        <button>
          go to uoload
        </button>
      </Link>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
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

import React, { useCallback, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AboutUs from './views/aboutus';
import Main from './views/main';
import Folder from './views/folderscreen2';
import File from './views/newfilescreen';
import Search from './views/newsearchscreen';
import Upload from './views/uploadscreen';
//import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        
        <div className="content">
        <Routes>
          <Route path="/" element={<Upload/>} />
          <Route path="/folders" element={<Folder/>} />
          <Route path="/about" element={<AboutUs />}/>
          <Route path="/filescreen" element={<File />}/>
          <Route path="/searchscreen" element={<Search />}/>
        </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

import React, { useCallback, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/header';
import AboutUs from './views/aboutus';
import Main from './views/main';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <div className="content">
        <Routes>
          <Route path="/" element={<Main/>} />
          <Route path="/about" element={<AboutUs />}/>
        </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

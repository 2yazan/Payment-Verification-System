import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import Header from './components/Header';
import DetailsPage from './components/DetailsPage';
import BuyPage from './components/BuyPage';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  return (
    <Router>
      <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/details" element={<DetailsPage />} />
          <Route path="/buy" element={<BuyPage />} />
        </Routes>
    </Router>
  );
}

export default App;
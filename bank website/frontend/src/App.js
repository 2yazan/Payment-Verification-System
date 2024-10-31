import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Home from './components/Home';
import Header from './components/Header'
import Payment from './components/Payment';
import PaymentHistory from './components/PaymentHistory';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  return (
    <Router>
      <Header />
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Home />} />
          <Route path="/Payment" element={<Payment />} />
          <Route path="/payment-history" element={<PaymentHistory />} />
        </Routes>
    </Router>
  );
}

export default App;


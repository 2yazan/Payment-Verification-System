import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Payment() {
  const [payerAccountNumber, setPayerAccountNumber] = useState('');
  const [receiver, setReceiver] = useState('');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://localhost:8000/api/account/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    .then(response => {
      console.log('Account details:', response.data);
      setPayerAccountNumber(response.data.account_number);
    })
    .catch(error => {
      console.error('Error fetching account details:', error);
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    
    if (!receiver || !amount || !description) {
      setErrors('All fields are required');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/api/payments/create/', {
        payer: payerAccountNumber,
        receiver,
        amount,
        description,
      }, {
        headers: {
          Authorization: `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });

      console.log('Payment successful:', response.data);
      navigate('/payment-history'); // Redirect to payment history after successful payment
    } catch (error) {
      console.error('Payment failed:', error);
      setErrors('Payment failed');
    }
  };

  return (
    <div className="main-content">
      <h2 className="page-title">Make a Payment</h2>
      {errors && <p className="error-message">{errors}</p>}
      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-group">
          <label>Receiver Account Number</label>
          <div className="input-container">
            <input
              type="text"
              value={receiver}
              onChange={(e) => setReceiver(e.target.value)}
              className="form-input"
            />
          </div>
        </div>
        <div className="form-group">
          <label>Amount</label>
          <div className="input-container">
            <input
              type="text"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="form-input"
            />
          </div>
        </div>
        <div className="form-group">
          <label>Description</label>
          <div className="input-container">
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="form-input"
            />
          </div>
        </div>
        <div className="form-group">
          <button type="submit" className="form-button">Submit Payment</button>
        </div>
      </form>
    </div>
  );
}

export default Payment;

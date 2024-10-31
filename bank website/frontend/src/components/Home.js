import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Home() {
  const [user, setUser] = useState(null);
  const [balance, setBalance] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    console.log('Token from localStorage:', token);
    if (token) {

      axios.get('http://localhost:8000/api/verify-token/', {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then(response => {
        console.log('Token is valid:', response.data);
        setUser(response.data.user);

        // Fetch user balance
        axios.get('http://localhost:8000/api/account/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        })
        .then(response => {
          setBalance(response.data.balance);
        })
        .catch(error => {
          console.error('Error fetching balance', error);
        });
      })
      .catch(error => {
        console.error('Invalid token', error);
        localStorage.removeItem('token');
        navigate('/login');
      });
    } else {
      navigate('/login');
    }
  }, [navigate]);

  const handlePaymentHistory = () => {
    navigate('/payment-history');
  };

  return (
    <div className="main-content">
      <div className="form-container">
        <h2 className="page-title">Hello {user ? user.username : ''}</h2>
        {balance !== null && (
          <p className="balance">Your balance: ${balance}</p>
        )}
        <button onClick={() => navigate('/payment')} className="home-button">
          Make a Payment
        </button>
        <button onClick={handlePaymentHistory} className="home-button">
          Payment History
        </button>
        <button onClick={() => { localStorage.removeItem('token'); navigate('/login'); }} className="home-button logout-button">
          Logout
        </button>
      </div>
    </div>
  );
}

export default Home;

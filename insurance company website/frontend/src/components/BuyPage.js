import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const BuyPage = () => {
  const location = useLocation();
  const { packagePrice } = location.state || { packagePrice: 0 };

  const [uploadError, setUploadError] = useState(null);
  const [paymentStatus, setPaymentStatus] = useState(null);

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) {
        setUploadError('Please select a file to upload.');
        return;
    }

    const formData = new FormData();
    formData.append('payment_check', file);
    formData.append('package_price', packagePrice);  // Include the package price in the request

    const csrftoken = getCookie('csrftoken');

    try {
        const response = await axios.post('http://127.0.0.1:8001/api/upload/payment-check/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrftoken
            }
        });

        const data = response.data;
        setUploadError(null);
        console.log('Upload successful:', data);

        if (data.verified) {
            if (data.sufficient) {
                setPaymentStatus('Payment is verified and sufficient!');
            } else {
                setPaymentStatus(`Payment is verified but insufficient. Amount paid: ${data.amount}, required: ${packagePrice}`);
            }
        } else {
            setPaymentStatus('Payment could not be verified.');
        }

    } catch (error) {
        console.error('Upload failed:', error);
        setUploadError('Error verifing file. Please try again.');
        setPaymentStatus(null);
    }
};


  return (
    <div className="buy-page-container">
      <div className="buy-box">
        <h2>Upload Your Payment Check</h2>
        <p>Amount to be paid: ${packagePrice}</p>
        <input type="file" accept="image/*,application/pdf" onChange={handleFileUpload} />
        {uploadError && <p className="error-message">{uploadError}</p>}
        {paymentStatus && <p className="success-message">{paymentStatus}</p>}
      </div>
    </div>
  );
};

export default BuyPage;

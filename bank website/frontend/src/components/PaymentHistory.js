import React, { useEffect, useState } from 'react';
import axios from 'axios';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { Modal, Box, Button, Typography } from '@mui/material';

function PaymentHistory({ user }) {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [selectedPayment, setSelectedPayment] = useState(null);

  const handleOpen = (payment) => {
    setSelectedPayment(payment);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Token not found');
      setLoading(false);
      return;
    }

    axios.get('http://localhost:8000/api/payments/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    .then(response => {
      setPayments(response.data);
      setLoading(false);
    })
    .catch(error => {
      console.error('Error fetching payment history:', error);
      setLoading(false);
    });
  }, []);

  const generateCheckContent = (payment) => `
    YBank

    TRANSACTION RECEIPT
    YBANK ONLINE

    TRANSACTION:
    PAYMENT FOR SERVICES
    TRANSACTION DATE:
    ${new Date(payment.date_time).toLocaleDateString()}
    TRANSACTION TIME:
    ${new Date(payment.date_time).toLocaleTimeString()}
    TRANSACTION AMOUNT:
    $${payment.amount}
    TRANSACTION NUMBER:
    ${payment.payment_number}
    SENDER:
    ${payment.payer_account_number}
    RECEIVER:
    ${payment.receiver_account_number}
    PURPOSE OF PAYMENT:
    ${payment.description}

    Thanks for using YBank
  `;

  const downloadCheck = async (payment, type) => {
    if (type === 'pdf') {
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'in',
        format: [3, 5], // Portrait orientation (tall and narrow)
      });
  
      const checkContent = generateCheckContent(payment);
      const lines = checkContent.split('\n');
  
      const lineHeight = 0.2;
      const pageWidth = doc.internal.pageSize.getWidth();
      const pageHeight = doc.internal.pageSize.getHeight();
  
      doc.setFontSize(12);
  
      let y = (pageHeight - (lines.length * lineHeight)) / 2;
  
      for (const line of lines) {
        const textWidth = doc.getStringUnitWidth(line) * doc.internal.getFontSize() / doc.internal.scaleFactor;
        const x = (pageWidth - textWidth) / 2;
        doc.text(line, x, y);
        y += lineHeight;
      }
  
      doc.save(`ybank_check_${payment.id}.pdf`);
    } else if (type === 'image') {
      const checkContent = generateCheckContent(payment);
  
      const element = document.createElement('div');
      element.style.width = '400px'; // Narrow width for portrait orientation
      element.style.height = '800px'; // Tall height
      element.style.padding = '20px';
      element.style.backgroundColor = 'white';
      element.style.fontFamily = 'monospace';
      element.style.fontSize = '14px';
      element.innerText = checkContent;
  
      document.body.appendChild(element);
  
      await html2canvas(element).then((canvas) => {
        const imgData = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.href = imgData;
        link.download = `ybank_check_${payment.id}.png`;
        link.click();
      });
  
      document.body.removeChild(element);
    }
  
    handleClose(); // Close modal after download
  };
  

  if (loading) {
    return <div className="main-content">Loading...</div>;
  }

  return (
    <div className="main-content">
      <h2 className="page-title">Payment History</h2>
      <br />
      <table>
        <thead>
          <tr>
            <th>Amount</th>
            <th>Payment Number</th>
            <th>Description</th>
            <th>Date/Time</th>
            <th>Receiver Account Number</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {payments.map(payment => (
            <tr key={payment.id}>
              <td>${payment.amount}</td>
              <td>{payment.payment_number}</td>
              <td>{payment.description}</td>
              <td>{new Date(payment.date_time).toLocaleString()}</td>
              <td>{payment.receiver_account_number}</td>
              <td>
                <button className="save-button" onClick={() => handleOpen(payment)}>Save Check</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <Modal open={open} onClose={handleClose}>
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 300,
          bgcolor: 'background.paper',
          border: '2px solid #000',
          boxShadow: 24,
          p: 4,
          textAlign: 'center',
        }}>
          <Typography variant="h6" component="h2">
            Download Check As:
          </Typography>
          <Button 
            variant="contained" 
            onClick={() => downloadCheck(selectedPayment, 'pdf')} 
            sx={{ mt: 2, mr: 1 }}
          >
            PDF
          </Button>
          <Button 
            variant="contained" 
            onClick={() => downloadCheck(selectedPayment, 'image')} 
            sx={{ mt: 2, ml: 1 }}
          >
            Image
          </Button>
        </Box>
      </Modal>
    </div>
  );
}

export default PaymentHistory;

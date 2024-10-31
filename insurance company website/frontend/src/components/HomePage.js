import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';

const HomePage = () => {
  const [insurancePackages, setInsurancePackages] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchInsurancePackages = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8001/api/insurance/');
        setInsurancePackages(response.data);
      } catch (error) {
        console.error('Error fetching insurance packages:', error);
      }
    };

    fetchInsurancePackages();
  }, []);

  const handleAboutClick = () => {
    navigate('/details');
  };

  const handleBuyClick = (packageId, packagePrice) => {
    navigate('/buy', { state: { packageId, packagePrice } });
  };

  return (
    <div className="main-content">
      <h1 className="text-center">WELCOME TO YInsurance WEBSITE</h1>
      <h3 className="packages-heading">Our Packages:</h3>
      <div className="card-container">
        {insurancePackages.map((insurancePackage) => (
          <Card key={insurancePackage.id} style={{ width: '18rem', height: '500px' }}>
            <div style={{ height: '300px', overflow: 'hidden' }}>
              <Card.Img
                variant="top"
                src={insurancePackage.cover}
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
            </div>
            <Card.Body>
              <Card.Title>{insurancePackage.package_name}</Card.Title>
              <Card.Text>{insurancePackage.description}</Card.Text>
            </Card.Body>
            <ListGroup className="list-group-flush">
              <ListGroup.Item>Price: ${insurancePackage.price}</ListGroup.Item>
              <ListGroup.Item>Coverage Limit: ${insurancePackage.coverage_limit}</ListGroup.Item>
            </ListGroup>
            <Card.Body>
              <Button 
                variant="primary" 
                onClick={() => handleBuyClick(insurancePackage.id, insurancePackage.price)}
              >
                Buy Package
              </Button>{' '}
              <Button variant="secondary" onClick={handleAboutClick}>details</Button>
            </Card.Body>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default HomePage;

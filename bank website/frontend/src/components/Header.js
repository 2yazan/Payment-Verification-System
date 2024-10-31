import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';

function Header() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <Navbar className="custom-bg-color" variant="dark">
      <Container>
        <Navbar.Brand as={Link} to="/">YBank</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Link as={Link} to="/">Home</Nav.Link>
          <Nav.Link as={Link} to="/Payment">Payments</Nav.Link>
          <Nav.Link as={Link} to="/payment-history">History</Nav.Link>
        </Nav>
        <Nav>
          <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  );
}

export default Header;

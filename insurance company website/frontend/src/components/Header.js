import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';


function Header() {
  return (
    <Navbar className = "custom-bg-color" variant="dark">
      <Container>
        <Navbar.Brand as={Link} to="/">YInsurance</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Link as={Link} to="/">history</Nav.Link>
          <Nav.Link as={Link} to="/">about us</Nav.Link>
        </Nav>
        <Nav>
        </Nav>
        
      </Container>
    </Navbar>
  );
}

export default Header;

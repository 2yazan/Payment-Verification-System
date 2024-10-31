import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setErrors('All fields are required');
      return;
    }
    try {
      const response = await axios.post('http://localhost:8000/api/register/', {
        username,
        password
      });
      console.log(response.data);
      setErrors('Registration successful, please login.');
    } catch (error) {
      setErrors('Registration failed');
      console.error(error);
    }
  };

  return (
    <div className="main-content">
      <div className="form-container">
        <h2 className="page-title">Register</h2>
        {errors && <p className="error-message">{errors}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="form-input"
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input"
            />
          </div>
          <button type="submit" className="form-button" style={{ width: '100%' }}>
            Register
          </button>
        </form>
        <p style={{ marginTop: '10px' }}>
          Already have an account? <Link to="/login">Click here to login</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;

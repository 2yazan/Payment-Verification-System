import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setErrors('All fields are required');
      return;
    }
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        username,
        password
      });
      const token = response.data.token;
      console.log('Token received from backend:', token);
      localStorage.setItem('token', token);
      navigate('/');
    } catch (error) {
      setErrors('Login failed');
      console.error(error);
    }
  };

  return (
    <div className="main-content">
      <div className="form-container">
        <h2 className="page-title">Login</h2>
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
            Login
          </button>
        </form>
        <p style={{ marginTop: '10px' }}>
          Don't have an account? <Link to="/register">Click here to register</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;

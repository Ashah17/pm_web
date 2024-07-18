import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import logo from './logo.png'; // Adjust the path as needed
import axios from 'axios'
import styled from 'styled-components'

const Button = styled.button`
  background-color: #0074D9;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  border-radius: 5px;
  cursor: pointer;
  &:hover {
    background-color: #0053a3;
  }
`;

function Header() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);


  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/session_info', { withCredentials: true });
        if (response.data) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        setIsAuthenticated(false);
      }
    };

    checkAuthStatus();
  }, []);

  const handleLogout = () => {
    window.location.href = 'http://localhost:8000/logout';
  };

  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/login';
  };

  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="PlanMaster Logo" />
      </div>
      <nav className="nav">
        <Link to="/">Create a Trip</Link>
        <Link to="/my-trips">My Trips</Link>
        <Link to="/my-account">My Account</Link>
        {isAuthenticated ? (
          <Button onClick={handleLogout}>Logout</Button>
        ) : (
          <Button onClick={handleLogin}>Login</Button>
        )}
      </nav>
    </header>
  );
}

export default Header;

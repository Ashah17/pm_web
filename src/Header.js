import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import logo from './logo.png'; // Adjust the path as needed

function Header() {
  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="PlanMaster Logo" />
      </div>
      <nav className="nav">
        <Link to="/">Create a Trip</Link>
        <Link to="/my-trips">My Trips</Link>
        <Link to="/my-account">My Account</Link>
      </nav>
    </header>
  );
}

export default Header;

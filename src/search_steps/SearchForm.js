// SearchForm.js
import React, { useState } from 'react';
import './SearchForm.css'; // Import the custom CSS for SearchForm

function SearchForm({ onSearch }) {
  const [location, setLocation] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const searchParams = { location, startDate, endDate };
    onSearch(searchParams);
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="input-container">
        <input 
          type="text" 
          value={location} 
          onChange={(e) => setLocation(e.target.value)} 
          placeholder="Enter location" 
          required 
        />
        <input 
          type="date" 
          value={startDate} 
          onChange={(e) => setStartDate(e.target.value)} 
          required 
        />
        <input 
          type="date" 
          value={endDate} 
          onChange={(e) => setEndDate(e.target.value)} 
          required 
        />
      </div>
      <div className="button-container">
        <button type="submit">Search</button>
      </div>
    </form>
  );
}

export default SearchForm;

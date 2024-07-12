import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchForm.css';
import LoadingSpinner from './LoadingSpinner'; // Import the LoadingSpinner component

function Step1LocationDate({ onSearch }) {
  const [location, setLocation] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(false); // Add loading state
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Set loading to true when starting search
    const searchParams = { location, startDate, endDate };
    await onSearch(searchParams);
    setLoading(false); // Set loading to false after search completes
    navigate('/itineraries'); // Navigate to itineraries after search
  };

  return (
    <>
      {loading && <LoadingSpinner />} {/* Show loading spinner when loading */}
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
          <button type="submit">Develop Options</button>
        </div>
      </form>
    </>
  );
}

export default Step1LocationDate;
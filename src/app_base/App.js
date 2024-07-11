import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './Header';
import Step1LocationDate from '../search_steps/Step1LocationDate';
import Step2Itineraries from '../search_steps/Step2Itineraries';
import Step3Map from '../search_steps/Step3Map';
import Step4Confirmation from '../search_steps/Step4Confirmation';
import AuthPage from '../user/AuthPage';
import ProfilePage from '../user/ProfilePage';
import './App.css';
import axios from 'axios';
import beachImage from './beach.png';
import LoadingSpinner from '../search_steps/LoadingSpinner'; // Assume you have a LoadingSpinner component

function App() {
  const [itineraries, setItineraries] = useState([]);
  const [selectedItinerary, setSelectedItinerary] = useState(null);
  const [loading, setLoading] = useState(false); // Add loading state

  useEffect(() => {
    fetchItineraries();
  }, []);

  const fetchItineraries = async () => {
    setLoading(true); // Set loading to true when fetching itineraries
    try {
      const response = await axios.get('http://localhost:8000/submit');
      setItineraries(response.data.itineraries);
    } catch (error) {
      console.error('Error fetching itineraries:', error);
    } finally {
      setLoading(false); // Set loading to false after fetching
    }
  };

  const handleSearch = async (params) => {
    setLoading(true); // Set loading to true when starting search
    const formData = {
      location: params.location,
      startDate: params.startDate,
      endDate: params.endDate
    };

    try {
      const response = await axios.post('http://localhost:8000/submit', formData);
      setItineraries(response.data.itineraries);
    } catch (error) {
      console.error('Error submitting search:', error);
    } finally {
      setLoading(false); // Set loading to false after search completes
    }
  };

  return (
    <Router>
      <div className="App">
        <Header />
        {loading && <LoadingSpinner />} {/* Show loading spinner when loading */}
        <Routes>
          <Route path="/" element={
            <div className="landing">
              <div className="landing-image-container">
                <img src={beachImage} alt="Beach" className="landing-image" />
                <div className="landing-image-overlay"></div>
              </div>
              <div className="landing-text">
                <h1>Ready to plan your perfect trip...</h1>
              </div>
              <div className="form-container">
                <Step1LocationDate onSearch={handleSearch} />
              </div>
            </div>
          } />
          <Route path="/itineraries" element={<Step2Itineraries itineraries={itineraries} setSelectedItinerary={setSelectedItinerary} setLoading={setLoading} />} />
          <Route path="/map" element={<Step3Map selectedItinerary={selectedItinerary} />} />
          <Route path="/confirmation" element={<Step4Confirmation />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/my-account" element={<ProfilePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

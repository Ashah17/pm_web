import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './Header';
import Step1LocationDate from './Step1LocationDate';
import Step2Itineraries from './Step2Itineraries';
import Step3Map from './Step3Map';
import Step4Confirmation from './Step4Confirmation';
import './App.css';
import axios from 'axios';
import beachImage from './beach.png';

function App() {
  const [itineraries, setItineraries] = useState([]);
  const [selectedItinerary, setSelectedItinerary] = useState(null); // State for selected itinerary

  useEffect(() => {
    fetchItineraries();
  }, []);

  const fetchItineraries = async () => {
    try {
      const response = await axios.get('http://localhost:8000/submit');
      setItineraries(response.data.itineraries); // Set itineraries from response
    } catch (error) {
      console.error('Error fetching itineraries:', error);
    }
  };

  const handleSearch = async (params) => {
    const formData = {
      location: params.location,
      startDate: params.startDate,
      endDate: params.endDate
    };

    try {
      const response = await axios.post('http://localhost:8000/submit', formData);
      setItineraries(response.data.itineraries); // Update itineraries on search
    } catch (error) {
      console.error('Error submitting search:', error);
    }
  };
  
  return (
    <Router>
      <div className="App">
        <Header />
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
          <Route path="/itineraries" element={<Step2Itineraries itineraries={itineraries} setSelectedItinerary={setSelectedItinerary} />} />
          <Route path="/map" element={<Step3Map selectedItinerary={selectedItinerary} />} />
          <Route path="/confirmation" element={<Step4Confirmation />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

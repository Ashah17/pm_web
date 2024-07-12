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
import { submitSearch } from '../search_steps/API.js'
import LoadingSpinner from '../search_steps/LoadingSpinner'; // Assume you have a LoadingSpinner component

function App() {
  //below are the states defined (js works on this to transfer info bw webpages)
  const [itineraries, setItineraries] = useState([]);
  const [selectedItinerary, setSelectedItinerary] = useState(null);
  const [detailedItinerary, setDetailedItinerary] = useState(null); //state + corresponding setter
  
  const [loading, setLoading] = useState(false); // loading state
  
  const handleSearch = async (params) => {
    setLoading(true);
    try {
      const data = await submitSearch(params);
      setItineraries(data);
    } catch (error) {
      console.error('Error submitting search:', error);
    } finally {
      setLoading(false);
    }
  }; //handles the submit endpoint logic

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
          <Route path="/itineraries" element=
            {<Step2Itineraries 
              itineraries={itineraries} 
              setSelectedItinerary={setSelectedItinerary} 
              setDetailedItinerary={setDetailedItinerary} //state functions
              setLoading={setLoading} />} />
          <Route path="/map" element={<Step3Map detailedItinerary={detailedItinerary}/>} />
          <Route path="/confirmation" element={<Step4Confirmation />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/my-account" element={<ProfilePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

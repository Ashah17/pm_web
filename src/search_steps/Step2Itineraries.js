import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Step2Itineraries.css';
import LoadingSpinner from './LoadingSpinner'; // Import the LoadingSpinner component

function Step2Itineraries({ itineraries, setSelectedItinerary }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSelectItinerary = async (itinerary) => {
    setLoading(true); // Set loading to true when starting the backend process

    setSelectedItinerary({
      name: `Option ${itinerary}`,
      description: itineraries[itinerary].map(([place, days]) => `${place} - ${days}`).join(', ')
    });

    try {
      const response = await fetch('http://localhost:8000/detailed_options', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedOption: itinerary,
          itineraries: itineraries
        })
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Selected Itinerary Details:', data);
        navigate('/map');
      } else {
        console.error('Error fetching detailed options:', data);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false); // Set loading to false after the backend process completes
    }
  };

  return (
    <div className="itineraries-container">
      <h2>Choose your favorite itinerary below...</h2>
      {loading && <LoadingSpinner />} {/* Show loading spinner when loading */}
      <div className="itinerary-options">
        {Object.keys(itineraries).map(optionNumber => (
          <div key={optionNumber} className="option-box" onClick={() => handleSelectItinerary(optionNumber)}>
            <h3>Option {optionNumber}</h3>
            <ul>
              {itineraries[optionNumber].map((placeInfo, index) => (
                <li key={index}>
                  <span className="place">{placeInfo[0]}</span> - <span className="days">{placeInfo[1]}</span>
                </li>
              ))}
            </ul>
            {/* Optionally, you can show placeholder or loading state for images */}
            {/* {itineraryImages[optionNumber] && (
              <img src={itineraryImages[optionNumber]} alt={`Image for Option ${optionNumber}`} className="itinerary-image" />
            )} */}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Step2Itineraries;

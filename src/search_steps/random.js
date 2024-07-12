
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from './LoadingSpinner'; // Import the LoadingSpinner component
import { detailedOptions } from '../search_steps/API'; // Adjust the import path as needed

function Step2Itineraries({ itineraries, setSelectedItinerary, setDetailedItinerary }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSelectItinerary = async (itinerary) => {
    setLoading(true); // Set loading to true when starting the backend process

    setSelectedItinerary({
      name: `Option ${itinerary}`,
      description: itineraries[itinerary].map(([place, days]) => `${place} - ${days}`).join(', ')
    });

    try {
      // Fetch detailed options from backend
      const detailedItinerary = await detailedOptions(itinerary, itineraries);
      setDetailedItinerary(detailedItinerary); // Save detailed itinerary to state
      navigate('/map'); // Navigate to the map page
    } catch (error) {
      console.error('Error fetching detailed options:', error);
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
          </div>
        ))}
      </div>
    </div>
  );
}

export default Step2Itineraries;

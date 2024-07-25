import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Step2Itineraries.css';
import LoadingSpinner from './LoadingSpinner'; // Import the LoadingSpinner component
import { detailedOptions } from './API'

function Step2Itineraries({ itineraries, setSelectedItinerary, setDetailedItinerary }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSelectedItinerary = async (itinerary) => {
    setLoading(true) //loading spinner

    const itinerary_selected = {
      name: `Option ${itinerary}`,
      description: itineraries[itinerary].map(([place, days]) => `${place} - ${days}`).join(', ')
    }; //set selected itinerary function

    setSelectedItinerary(itinerary_selected)

    try {
      //get details from backend endpoint
      const detailedItinerary = await detailedOptions(itinerary, itineraries);
      //passing in the itinerary (optionChosen) and itineraries dict to backend as params
      setDetailedItinerary(detailedItinerary); //save to state
      navigate('/map'); //navigate to map
    } catch (error) {
      console.error('error fetching details');
    } finally {
      setLoading(false); //either way loading done
    }
  };

  return (
    <div className="itineraries-container">
      <h2>Choose your favorite itinerary below...</h2>
      {loading && <LoadingSpinner />} {/* Show loading spinner when loading */}
      <div className="itinerary-options">
        {Object.keys(itineraries).map(optionNumber => (
          <div key={optionNumber} className="option-box" onClick={() => handleSelectedItinerary(optionNumber)}>
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

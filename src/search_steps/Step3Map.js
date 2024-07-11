import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function Step3Map({ selectedItinerary }) {
  const navigate = useNavigate();
  const location = useLocation();
  const detailedItinerary = location.state ? location.state.detailedItinerary : null;

  const handleConfirm = () => {
    navigate('/confirmation');
  };

  if (!selectedItinerary) {
    return <p>No itinerary selected</p>;
  }

  return (
    <div>
      <h2>View Itinerary on Map</h2>
      <p>{selectedItinerary.name}</p>
      <p>{selectedItinerary.description}</p>
      {/* Display the detailed itinerary */}
      {Array.isArray(detailedItinerary) ? (
        <div>
          <h3>Detailed Itinerary</h3>
          <ul>
            {detailedItinerary.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p>{detailedItinerary}</p>
      )}
      <button onClick={handleConfirm}>Confirm</button>
    </div>
  );
}

export default Step3Map;

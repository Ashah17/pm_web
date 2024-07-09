import React from 'react';
import { useNavigate } from 'react-router-dom';

function Step3Map({ selectedItinerary }) {
  const navigate = useNavigate();

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
      {/* You would integrate a map component here */}
      <button onClick={handleConfirm}>Confirm</button>
    </div>
  );
}

export default Step3Map;

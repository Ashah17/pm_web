import React from 'react';

function Step4Confirmation({ itinerary, searchParams }) {
  if (!itinerary) {
    return <p>No itinerary selected</p>;
  }

  return (
    <div>
      <h2>Confirmation</h2>
      <p>Location: {searchParams.location}</p>
      <p>Start Date: {searchParams.startDate}</p>
      <p>End Date: {searchParams.endDate}</p>
      <p>Itinerary: {itinerary.name}</p>
      <p>Description: {itinerary.description}</p>
      {/* Additional confirmation details here */}
    </div>
  );
}

export default Step4Confirmation;

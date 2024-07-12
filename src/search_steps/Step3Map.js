import React, { useState } from 'react';
import './Step3Map.css'; // Ensure you have this CSS file

function Step3Map({ detailedItinerary }) {
  const [expandedKey, setExpandedKey] = useState(null);

  const handleExpand = (key) => {
    setExpandedKey(expandedKey === key ? null : key);
  };

  if (!detailedItinerary || Object.keys(detailedItinerary).length === 0) {
    return <div>No detailed itinerary available.</div>;
  }

  return (
    <div className="map-container">
      <div className="itinerary-details">
        {Object.keys(detailedItinerary).map((key) => (
          <div key={key} className="itinerary-section">
            <div className="section-header" onClick={() => handleExpand(key)}>
              <span className="expand-icon">
                {expandedKey === key ? '-' : '+'}
              </span>
              <h3>{key}</h3>
            </div>
            {expandedKey === key && (
              <div className="section-content">
                <div className="content-box">
                  <h4>Places</h4>
                  <ul>
                    {detailedItinerary[key][0].map((place, index) => (
                      <li key={index}>{place}</li>
                    ))}
                  </ul>
                </div>
                <div className="content-box">
                  <h4>Restaurants</h4>
                  <ul>
                    {detailedItinerary[key][1].map((restaurant, index) => (
                      <li key={index}>{restaurant}</li>
                    ))}
                  </ul>
                </div>
                <div className="content-box">
                  <h4>Tips</h4>
                  <ul>
                    {detailedItinerary[key][2].map((tip, index) => (
                      <li key={index}>{tip}</li>
                    ))}
                  </ul>
                </div>
                <div className="content-box">
                  <h4>Transportation</h4>
                  <ul>
                    {detailedItinerary[key][3].map((transport, index) => (
                      <li key={index}>{transport}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="map-placeholder">
        {/* Replace this with your actual map */}
        <div className="map-content">Map Placeholder</div>
      </div>
    </div>
  );
}

export default Step3Map;

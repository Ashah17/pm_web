import React, { useState } from 'react';
import './Step3Map.css'; // Ensure this file includes the custom checkbox styles
import { useNavigate } from 'react-router-dom';
import { mappingDetails } from './API';

function Step3Map({ detailedItinerary, selectedItinerary, setBuiltItinerary, setMappingData }) {
  const navigate = useNavigate();
  const [expandedKey, setExpandedKey] = useState(null);
  const [placeholders, setPlaceholders] = useState({});
  const [loading, setLoading] = useState(false); // Add loading state
  const [filled, setFilled] = useState(false); // Track whether checkboxes should be filled

  const handleExpand = (key) => {
    setExpandedKey(expandedKey === key ? null : key);
  };

  const handleCheckboxChange = (key, item, type) => {
    setPlaceholders((prev) => {
      const currentItems = prev[key]?.[type] || [];
      const updatedItems = currentItems.includes(item)
        ? currentItems.filter((i) => i !== item)
        : [...currentItems, item];

      return {
        ...prev,
        [key]: {
          ...prev[key],
          [type]: updatedItems,
        },
      };
    });
  };

  

  const handleConfirm = async () => {
    setLoading(true); // Set loading state
    setFilled(true); // Set filled state to true

    const formattedData = Object.keys(placeholders).reduce((acc, key) => {
      acc[key] = [
        placeholders[key]?.places || [],
        placeholders[key]?.restaurants || []
      ];
      return acc;
    }, {});

    try {
      console.log('Sending data to server:', formattedData); // Debug log
      const itinerary_and_mapping = await mappingDetails(formattedData, selectedItinerary); // BOTH details AND mapping data
      
      // const builtItinerary = itinerary_and_mapping.mappingDetails
      // const mappingData = itinerary_and_mapping.mappingData

      const { mappingDetails: builtItinerary, mappingData: mappingData } = itinerary_and_mapping;

      console.log('Received user built itinerary from server:', builtItinerary); // Debug log

      console.log('Received mapping data from server:', mappingData); // Debug log for mapping data

      setBuiltItinerary(builtItinerary); // Save response to state
      setMappingData(mappingData)
      navigate('/confirmation'); // Navigate to confirmation page

    } catch (error) {
      console.error('Error sending data to the server:', error); // Error handling
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  if (!detailedItinerary || Object.keys(detailedItinerary).length === 0) {
    return <div>No detailed itinerary available.</div>; // Handle empty itinerary
  }

  return (
    <div className="map-container">
      {loading && <div className="loading-spinner">Loading...</div>} {/* Show loading spinner */}
      <button className="magic-button">
        <span role="img" aria-label="wand">✨</span> Let PlanMaster do its magic (beta)
      </button>
      <div className="left-side">
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
                {['Places', 'Restaurants'].map((type, index) => (
                  <div className="content-box" key={index}>
                    <h4>{type}</h4>
                    <ul>
                      {detailedItinerary[key][index].map((item, idx) => (
                        <li key={idx}>
                          <input
                            type="checkbox"
                            className="circular-checkbox"
                            checked={placeholders[key]?.[type]?.includes(item) || false}
                            onChange={() => handleCheckboxChange(key, item, type.toLowerCase())}
                          />
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="right-side">
        {Object.keys(detailedItinerary).map((key) => (
          <div key={key} className="placeholder-box">
            <h3>{key}</h3>
            <div className="placeholder-section">
              <h4>Places</h4>
              <ul>
                {placeholders[key]?.places?.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="placeholder-section">
              <h4>Restaurants</h4>
              <ul>
                {placeholders[key]?.restaurants?.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
      <button className="confirm-button" onClick={handleConfirm} disabled={loading}>
        {loading ? 'Confirming...' : 'Confirm'} {/* Disable button while loading */}
      </button>
    </div>
  );
}

export default Step3Map;

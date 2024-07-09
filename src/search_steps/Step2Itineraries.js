import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Step2Itineraries.css';
import fetchImage from './unsplashAPI'; // Assuming you have a function to fetch images from Unsplash

function Step2Itineraries({ itineraries, setSelectedItinerary }) {
  const navigate = useNavigate();
  const [itineraryImages, setItineraryImages] = useState({});

  // Function to handle selecting an itinerary
  const handleSelectItinerary = async (itinerary) => {
    setSelectedItinerary({
      name: `Option ${itinerary}`,
      description: itineraries[itinerary].map(([place, days]) => `${place} - ${days}`).join(', ')
    });
    navigate('/map');
  };

  // Effect to load images for each itinerary option
  // useEffect(() => {
  //   const loadImages = async () => {
  //     const images = {};
  //     for (let i = 0; i < Object.keys(itineraries).length; i++) {
  //       const locationName = itineraries[i + 1][0][0];
  //       try {
  //         const imageUrl = await fetchImage(locationName); // Assuming fetchImage returns a URL
  //         images[i + 1] = imageUrl;
  //       } catch (error) {
  //         console.error(`Error fetching image for ${locationName}:`, error);
  //         // Handle error, maybe set a placeholder image or skip this image
  //       }
  //     }
  //     setItineraryImages(images);
  //   };
  //   loadImages();
  // }, [itineraries]);

  return (
    <div className="itineraries-container">
      <h2>Choose your favorite itinerary below...</h2>
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
            {itineraryImages[optionNumber] && (
              <img src={itineraryImages[optionNumber]} alt={`Image for Option ${optionNumber}`} className="itinerary-image" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Step2Itineraries;



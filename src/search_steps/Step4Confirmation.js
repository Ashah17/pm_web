// import React from 'react';
// import { useNavigate } from 'react-router-dom';


// function Step4Confirmation({ builtItinerary }) {
//   const navigate = useNavigate();

//   if (!builtItinerary || Object.keys(builtItinerary).length === 0) {
//     return <p>No itinerary returned.</p>; // Handle case with no itinerary
//   }

//   const handleGoBack = () => {
//     navigate('/map'); // Navigate back to the map page
//   };

//   return (
//     <div className="confirmation-container">
//       <button className="back-button" onClick={handleGoBack}>
//         Go back to edit my itinerary
//       </button>
//       <h2>Confirmation</h2>
//       {Object.keys(builtItinerary).map((key) => (
//         <div key={key} className="itinerary-section">
//           <h3>{key}</h3>
//           <div className="confirmation-content">
//             <div className="confirmation-box">
//               <h4>Duration</h4>
//               <p>{builtItinerary[key][0]} day(s)</p>
//             </div>
//             <div className="confirmation-box">
//               <h4>Places</h4>
//               <ul>
//                 {builtItinerary[key][1].map((item, index) => (
//                   <li key={index}>{item}</li>
//                 ))}
//               </ul>
//             </div>
//             <div className="confirmation-box">
//               <h4>Restaurants</h4>
//               <ul>
//                 {builtItinerary[key][2].map((item, index) => (
//                   <li key={index}>{item}</li>
//                 ))}
//               </ul>
//             </div>
//           </div>
//         </div>
//       ))}
//       {/* Additional confirmation details can be added here */}
//     </div>
//   );
// }

// export default Step4Confirmation;
import React from 'react';
import { useNavigate } from 'react-router-dom';
import MapComponent from './MapComponent';

function Step4Confirmation({ builtItinerary, mappingData }) {
  const navigate = useNavigate();

  if (!builtItinerary || Object.keys(builtItinerary).length === 0) {
    return <p>No itinerary returned.</p>;
  }

  const handleGoBack = () => {
    navigate('/map');
  };

  return (
    <div className="confirmation-container">
      <button className="back-button" onClick={handleGoBack}>
        Go back to edit my itinerary
      </button>
      <h2>Confirmation</h2>
      {Object.keys(builtItinerary).map((key) => (
        <div key={key} className="itinerary-section">
          <h3>{key}</h3>
          <div className="confirmation-content">
            <div className="confirmation-box">
              <h4>Duration</h4>
              <p>{builtItinerary[key][0]} day(s)</p>
            </div>
            <div className="confirmation-box">
              <h4>Places</h4>
              <ul>
                {builtItinerary[key][1].map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="confirmation-box">
              <h4>Restaurants</h4>
              <ul>
                {builtItinerary[key][2].map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="confirmation-box">
              <h4>Map</h4>
              {mappingData[key] ? (
                <MapComponent mappingData={mappingData[key]} />
              ) : (
                <p>No map data available for {key}</p>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default Step4Confirmation;

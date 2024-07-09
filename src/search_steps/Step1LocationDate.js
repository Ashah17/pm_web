// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import './SearchForm.css';
// import ProgressBar from './ProgressBar';

// function Step1LocationDate({ onSearch }) {
//   const [location, setLocation] = useState('');
//   const [startDate, setStartDate] = useState('');
//   const [endDate, setEndDate] = useState('');
//   const navigate = useNavigate();

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const searchParams = { location, startDate, endDate };
//     await onSearch(searchParams);
//     navigate('/itineraries');

//     const formData = {
//       location: state.location,
//       startDate: state.startDate,
//       endDate: state.endDate
//     };

//     try {
//       const response = await fetch('http://localhost:8000/submit', {
//           method: 'POST',
//           headers: {
//               'Content-Type': 'application/json',
//           },
//           body: JSON.stringify(formData),
//       });

//       // Check if the request was successful
//       if (response.ok) {
//           // Handle success
//           console.log('Form submitted successfully!');
//           // Reset the form fields if needed
//           this.setState({
//               location: "",
//               startDate: "",
//               endDate: ""
//           });

//           window.location.href = '/Step1LocationDate';
//       } else {
//           // Handle error
//           console.error('Error submitting form.');
//       }
//   } catch (error) {
//       // Handle unexpected error
//       console.error('An unexpected error occurred:', error);
//   }
  
//   // Send a POST request to the server

// };


    
  

//   return (
//     <form onSubmit={handleSubmit} className="search-form">
//       <div className="input-container">
//         <input 
//           type="text" 
//           value={location} 
//           onChange={(e) => setLocation(e.target.value)} 
//           placeholder="Enter location" 
//           required 
//         />
//         <input 
//           type="date" 
//           value={startDate} 
//           onChange={(e) => setStartDate(e.target.value)} 
//           required 
//         />
//         <input 
//           type="date" 
//           value={endDate} 
//           onChange={(e) => setEndDate(e.target.value)} 
//           required 
//         />
//       </div>
//       <div className="button-container">
//         <button type="submit">Next</button>
//       </div>
//     </form>
//   );
// }


// export default Step1LocationDate;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchForm.css';

function Step1LocationDate({ onSearch }) {
  const [location, setLocation] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const searchParams = { location, startDate, endDate };
    await onSearch(searchParams);
    navigate('/itineraries'); // Navigate to itineraries after search
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="input-container">
        <input
          type="text" 
          value={location} 
          onChange={(e) => setLocation(e.target.value)} 
          placeholder="Enter location" 
          required 
        />
        <input 
          type="date" 
          value={startDate} 
          onChange={(e) => setStartDate(e.target.value)} 
          required 
        />
        <input 
          type="date" 
          value={endDate} 
          onChange={(e) => setEndDate(e.target.value)} 
          required 
        />
      </div>
      <div className="button-container">
        <button type="submit">Develop Options</button>
      </div>
    </form>
  );
}

export default Step1LocationDate;

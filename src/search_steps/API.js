//file to centralize all API calls for organization + redundancy reduction

import axios from 'axios';

export const submitSearch = async (params) => {
    const response = await axios.post('http://localhost:8000/submit', params); //sends params as post req to submit endpoint
    return response.data.itineraries; //response is awaited, then data.itineraries is returned
}

export const detailedOptions = async (selectedOption, itineraries) => {
    const response = await axios.post('http://localhost:8000/detailed_options', {
        selectedOption,
        itineraries
    }); //sends selectedOption and the itineraries to detailed_options endpoint

    //in this case the params is the selected itinerary from the web page

    return response.data.listedItinerary; //listedItinerary is the response
}

export const mappingDetails = async (builtItinerary) => {
    const response = await axios.post('http://localhost:8000/mapping_details', builtItinerary);
    return response.data.mappingDetails;
}


import axios from 'axios';

const UNSPLASH_ACCESS_KEY = 'MM3xFWTClUaoucenDafTi1DkUMupOpQKBstSNk78Ltc';

const fetchImage = async (query) => {
  try {
    const response = await axios.get('https://api.unsplash.com/search/photos', {
      params: { query, per_page: 1 },
      headers: {
        Authorization: `Client-ID ${UNSPLASH_ACCESS_KEY}`
      }
    });
    const imageUrl = response.data.results[0]?.urls?.small;
    return imageUrl;
  } catch (error) {
    console.error('Error fetching image:', error);
    return null;
  }
};

export default fetchImage;

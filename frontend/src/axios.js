import axios from 'axios';

// Create a custom Axios instance
const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Your backend URL
  timeout: 5000, // Request timeout
});

// Add request interceptor (optional)
instance.interceptors.request.use(
  (config) => {
    // Add headers, authentication tokens, etc.
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor (optional)
instance.interceptors.response.use(
  (response) => {
    // Handle successful responses
    return response;
  },
  (error) => {
    // Handle errors (e.g., redirect to login on 401)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default instance;
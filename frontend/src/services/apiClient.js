/**
 * Cliente Axios configurado para la API del backend.
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env?.VITE_API_BASE || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores globalmente
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMessage = error.response?.data?.error || error.message || 'Error desconocido';
    console.error('API Error:', errorMessage);
    return Promise.reject(error);
  }
);

export default apiClient;

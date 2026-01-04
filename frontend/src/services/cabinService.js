/**
 * Servicio para gestionar cabañas.
 */
import apiClient from './apiClient';

export const cabinService = {
  /**
   * Obtiene todas las cabañas.
   */
  getAll: async () => {
    const response = await apiClient.get('/cabins');
    return response.data.data;
  },

  /**
   * Obtiene una cabaña por ID.
   */
  getById: async (cabinId) => {
    const response = await apiClient.get(`/cabins/${cabinId}`);
    return response.data.data;
  },

  /**
   * Obtiene cabañas por grupo de par.
   */
  getByPair: async (pairGroup) => {
    const response = await apiClient.get(`/cabins/pair/${pairGroup}`);
    return response.data.data;
  },

  /**
   * Actualiza una cabaña.
   */
  update: async (cabinId, data) => {
    const response = await apiClient.put(`/cabins/${cabinId}`, data);
    return response.data.data;
  },
};

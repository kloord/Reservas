/**
 * Servicio para gestionar reservas.
 */
import apiClient from './apiClient';

export const reservationService = {
  /**
   * Obtiene todas las reservas.
   * @param {Object} filters - Filtros opcionales { cabin_id, start_date, end_date }
   */
  getAll: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.cabin_id) params.append('cabin_id', filters.cabin_id);
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.guest_name) params.append('guest_name', filters.guest_name);

    const response = await apiClient.get(`/reservations?${params.toString()}`);
    return response.data.data;
  },

  /**
   * Busca reservas por nombre de huésped (substring, case-insensitive).
   */
  searchByGuestName: async (name) => {
    const params = new URLSearchParams();
    if (name) params.append('guest_name', name);
    const response = await apiClient.get(`/reservations?${params.toString()}`);
    return response.data.data;
  },

  /**
   * Obtiene una reserva por ID.
   */
  getById: async (reservationId) => {
    const response = await apiClient.get(`/reservations/${reservationId}`);
    return response.data.data;
  },

  /**
   * Crea una nueva reserva.
   */
  create: async (reservationData) => {
    const response = await apiClient.post('/reservations', reservationData);
    return response.data.data;
  },

  /**
   * Actualiza una reserva existente.
   */
  update: async (reservationId, updateData) => {
    const response = await apiClient.put(`/reservations/${reservationId}`, updateData);
    return response.data.data;
  },

  /**
   * Elimina una reserva.
   */
  delete: async (reservationId) => {
    const response = await apiClient.delete(`/reservations/${reservationId}`);
    return response.data.data;
  },
};

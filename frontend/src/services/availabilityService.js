/**
 * Servicio para consultar disponibilidad de cabañas.
 */
import apiClient from './apiClient';

export const availabilityService = {
  /**
   * Consulta la disponibilidad de cabañas en un rango de fechas.
   * @param {string} startDate - Fecha de inicio (YYYY-MM-DD)
   * @param {string} endDate - Fecha de término (YYYY-MM-DD)
   * @param {number} cabinId - ID de cabaña específica (opcional)
   */
  checkAvailability: async (startDate, endDate, cabinId = null) => {
    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
    });

    if (cabinId) {
      params.append('cabin_id', cabinId);
    }

    const response = await apiClient.get(`/availability?${params.toString()}`);
    return response.data.data;
  },

  /**
   * Obtiene un resumen de disponibilidad.
   * @param {string} startDate - Fecha de inicio (YYYY-MM-DD)
   * @param {string} endDate - Fecha de término (YYYY-MM-DD)
   */
  getSummary: async (startDate, endDate) => {
    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
    });

    const response = await apiClient.get(`/availability/summary?${params.toString()}`);
    return response.data.data;
  },
};

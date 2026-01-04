/**
 * Componente ReservationModal - Modal para crear/editar reservas.
 */
import { useState, useEffect } from 'react';
import { reservationService } from '../services/reservationService';
import { formatDateForDisplay, formatDateToISO } from '../utils/dateUtils';
import './ReservationModal.css';

const ReservationModal = ({ 
  isOpen, 
  onClose, 
  cabin, 
  startDate, 
  endDate, 
  existingReservation = null,
  onSuccess 
}) => {
  const [formData, setFormData] = useState({
    guest_name: '',
    guest_email: '',
    guest_phone: '',
    num_guests: 1,
    notes: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (existingReservation) {
      setFormData({
        guest_name: existingReservation.guest_name || '',
        guest_email: existingReservation.guest_email || '',
        guest_phone: existingReservation.guest_phone || '',
        num_guests: existingReservation.num_guests || 1,
        notes: existingReservation.notes || ''
      });
    } else {
      setFormData({
        guest_name: '',
        guest_email: '',
        guest_phone: '',
        num_guests: 1,
        notes: ''
      });
    }
    setError('');
  }, [existingReservation, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const reservationData = {
        cabin_id: cabin.id,
        guest_name: formData.guest_name.trim(),
        guest_email: formData.guest_email.trim(),
        guest_phone: formData.guest_phone.trim(),
        start_date: existingReservation ? existingReservation.start_date : startDate,
        end_date: existingReservation ? existingReservation.end_date : endDate,
        num_guests: parseInt(formData.num_guests),
        notes: formData.notes.trim()
      };

      if (existingReservation) {
        await reservationService.update(existingReservation.id, reservationData);
      } else {
        await reservationService.create(reservationData);
      }

      onSuccess();
      onClose();
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Error al procesar la reserva';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!existingReservation) return;
    
    if (!window.confirm('¿Está seguro que desea eliminar esta reserva?')) {
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      await reservationService.delete(existingReservation.id);
      onSuccess();
      onClose();
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Error al eliminar la reserva';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const modalTitle = existingReservation ? 'Editar Reserva' : 'Nueva Reserva';
  const displayStartDate = existingReservation ? existingReservation.start_date : startDate;
  const displayEndDate = existingReservation ? existingReservation.end_date : endDate;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{modalTitle}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="reservation-summary">
            <h3>📍 {cabin.name}</h3>
            <div className="date-display">
              <strong>Fechas:</strong> {formatDateForDisplay(displayStartDate)} - {formatDateForDisplay(displayEndDate)}
            </div>
            <div className="capacity-display">
              <strong>Capacidad:</strong> {cabin.capacity} personas
            </div>
          </div>

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="label" htmlFor="guest_name">
                Nombre del Huésped <span className="required">*</span>
              </label>
              <input
                id="guest_name"
                name="guest_name"
                type="text"
                className="input"
                value={formData.guest_name}
                onChange={handleChange}
                required
                disabled={isSubmitting}
                placeholder="Ej: Juan Pérez"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="label" htmlFor="guest_email">Email</label>
                <input
                  id="guest_email"
                  name="guest_email"
                  type="email"
                  className="input"
                  value={formData.guest_email}
                  onChange={handleChange}
                  disabled={isSubmitting}
                  placeholder="correo@ejemplo.com"
                />
              </div>

              <div className="form-group">
                <label className="label" htmlFor="guest_phone">Teléfono</label>
                <input
                  id="guest_phone"
                  name="guest_phone"
                  type="tel"
                  className="input"
                  value={formData.guest_phone}
                  onChange={handleChange}
                  disabled={isSubmitting}
                  placeholder="+56 9 1234 5678"
                />
              </div>
            </div>

            <div className="form-group">
              <label className="label" htmlFor="num_guests">
                Número de Personas <span className="required">*</span>
              </label>
              <input
                id="num_guests"
                name="num_guests"
                type="number"
                className="input"
                value={formData.num_guests}
                onChange={handleChange}
                required
                min="1"
                max={cabin.capacity}
                disabled={isSubmitting}
              />
              <small className="text-muted">Máximo: {cabin.capacity} personas</small>
            </div>

            <div className="form-group">
              <label className="label" htmlFor="notes">Notas Adicionales</label>
              <textarea
                id="notes"
                name="notes"
                className="input textarea"
                value={formData.notes}
                onChange={handleChange}
                disabled={isSubmitting}
                rows="3"
                placeholder="Información adicional sobre la reserva..."
              />
            </div>

            <div className="modal-footer">
              {existingReservation && (
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={handleDelete}
                  disabled={isSubmitting}
                >
                  🗑️ Eliminar
                </button>
              )}
              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={onClose}
                  disabled={isSubmitting}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Guardando...' : existingReservation ? 'Actualizar' : 'Crear Reserva'}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ReservationModal;

import React from 'react'
import { formatDateForDisplay } from '../utils/dateUtils'
import './ReservationDetailsModal.css'

const ReservationDetailsModal = ({ reservation, cabinName, onClose }) => {
  if (!reservation) return null
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Detalle de Reserva</h3>
          <button className="btn btn-secondary" onClick={onClose}>Cerrar</button>
        </div>
        <div className="modal-body">
          <div className="detail-row">
            <span className="label">Cabaña:</span>
            <span className="value">{cabinName || `Cabaña ${reservation.cabin_id}`}</span>
          </div>
          <div className="detail-row">
            <span className="label">Huésped:</span>
            <span className="value">{reservation.guest_name}</span>
          </div>
          {reservation.guest_email && (
            <div className="detail-row">
              <span className="label">Email:</span>
              <span className="value">{reservation.guest_email}</span>
            </div>
          )}
          {reservation.guest_phone && (
            <div className="detail-row">
              <span className="label">Teléfono:</span>
              <span className="value">{reservation.guest_phone}</span>
            </div>
          )}
          <div className="detail-row">
            <span className="label">Entrada:</span>
            <span className="value">{formatDateForDisplay(reservation.start_date)}</span>
          </div>
          <div className="detail-row">
            <span className="label">Salida:</span>
            <span className="value">{formatDateForDisplay(reservation.end_date)}</span>
          </div>
          <div className="detail-row">
            <span className="label">Personas:</span>
            <span className="value">{reservation.num_guests}</span>
          </div>
          {reservation.notes && (
            <div className="detail-row">
              <span className="label">Notas:</span>
              <span className="value">{reservation.notes}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ReservationDetailsModal

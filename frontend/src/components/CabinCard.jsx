/**
 * Componente CabinCard - Tarjeta individual de cabaña.
 */
import './CabinCard.css';

const CabinCard = ({ cabin, isAvailable, currentReservation, onReserve, onViewDetails }) => {
  const statusClass = isAvailable ? 'available' : 'occupied';
  const statusText = isAvailable ? 'Disponible' : 'Ocupada';
  const statusIcon = isAvailable ? '✓' : '✕';

  return (
    <div className={`cabin-card ${statusClass}`}>
      <div className="cabin-card-header">
        <h3 className="cabin-name">{cabin.name}</h3>
        <span className={`status-badge ${statusClass}`}>
          {statusIcon} {statusText}
        </span>
      </div>

      {/* Se eliminan detalles: ID, Par, Capacidad y Amenidades */}
      <div className="cabin-card-body" />

      <div className="cabin-card-footer">
        {isAvailable ? (
          <button 
            className="btn btn-primary btn-sm cabin-action-btn"
            onClick={() => onReserve(cabin)}
          >
            📅 Reservar
          </button>
        ) : (
          <button 
            className="btn btn-secondary btn-sm cabin-action-btn"
            onClick={() => onViewDetails(currentReservation)}
          >
            👁️ Ver Detalles
          </button>
        )}
      </div>
    </div>
  );
};

export default CabinCard;

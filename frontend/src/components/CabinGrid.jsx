/**
 * Componente CabinGrid - Grid de cabañas con estado de disponibilidad.
 */
import CabinCard from './CabinCard';
import './CabinGrid.css';

const CabinGrid = ({ cabinsData, onReserve, onViewDetails, isLoading }) => {
  if (isLoading) {
    return (
      <div className="cabin-grid-loading">
        <div className="spinner"></div>
        <p>Cargando disponibilidad...</p>
      </div>
    );
  }

  if (!cabinsData || cabinsData.length === 0) {
    return (
      <div className="cabin-grid-empty">
        <p>No se encontraron cabañas.</p>
      </div>
    );
  }

  const availableCount = cabinsData.filter(c => c.is_available).length;
  const occupiedCount = cabinsData.length - availableCount;

  return (
    <div className="cabin-grid-container">
      <div className="cabin-grid-header">
        <h2 className="grid-title">Estado de Cabañas</h2>
        <div className="availability-summary">
          <div className="summary-item available">
            <span className="summary-count">{availableCount}</span>
            <span className="summary-label">Disponibles</span>
          </div>
          <div className="summary-item occupied">
            <span className="summary-count">{occupiedCount}</span>
            <span className="summary-label">Ocupadas</span>
          </div>
        </div>
      </div>

      <div className="cabin-grid">
        {cabinsData.map((cabinData) => (
          <CabinCard
            key={cabinData.cabin.id}
            cabin={cabinData.cabin}
            isAvailable={cabinData.is_available}
            currentReservation={cabinData.current_reservation}
            onReserve={onReserve}
            onViewDetails={onViewDetails}
          />
        ))}
      </div>
    </div>
  );
};

export default CabinGrid;

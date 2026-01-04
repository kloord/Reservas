/**
 * Componente DateRangeSelector - Selector de rango de fechas.
 */
import { useState, useEffect } from 'react';
import { getTodayISO, getTomorrowISO, isValidDateRange, daysBetween } from '../utils/dateUtils';
import './DateRangeSelector.css';

const DateRangeSelector = ({ onDateChange, initialStartDate, initialEndDate }) => {
  const [startDate, setStartDate] = useState(initialStartDate || getTodayISO());
  const [endDate, setEndDate] = useState(initialEndDate || getTomorrowISO());
  const [error, setError] = useState('');

  useEffect(() => {
    validateAndNotify();
  }, []);

  const validateAndNotify = () => {
    if (!startDate || !endDate) {
      setError('Ambas fechas son requeridas');
      return;
    }

    if (!isValidDateRange(startDate, endDate)) {
      setError('La fecha de inicio debe ser anterior a la fecha de término');
      return;
    }

    setError('');
    onDateChange({ startDate, endDate });
  };

  const handleStartDateChange = (e) => {
    const newStartDate = e.target.value;
    setStartDate(newStartDate);
    
    if (newStartDate && endDate) {
      if (!isValidDateRange(newStartDate, endDate)) {
        setError('La fecha de inicio debe ser anterior a la fecha de término');
      } else {
        setError('');
        onDateChange({ startDate: newStartDate, endDate });
      }
    }
  };

  const handleEndDateChange = (e) => {
    const newEndDate = e.target.value;
    setEndDate(newEndDate);
    
    if (startDate && newEndDate) {
      if (!isValidDateRange(startDate, newEndDate)) {
        setError('La fecha de inicio debe ser anterior a la fecha de término');
      } else {
        setError('');
        onDateChange({ startDate, endDate: newEndDate });
      }
    }
  };

  const days = startDate && endDate && isValidDateRange(startDate, endDate) 
    ? daysBetween(startDate, endDate) 
    : 0;

  return (
    <div className="date-range-selector card">
      <h2 className="selector-title">Seleccionar Rango de Fechas</h2>
      
      <div className="date-inputs">
        <div className="form-group">
          <label className="label" htmlFor="start-date">Fecha de Inicio</label>
          <input
            id="start-date"
            type="date"
            className="input"
            value={startDate}
            onChange={handleStartDateChange}
            min={getTodayISO()}
          />
        </div>

        <div className="form-group">
          <label className="label" htmlFor="end-date">Fecha de Término</label>
          <input
            id="end-date"
            type="date"
            className="input"
            value={endDate}
            onChange={handleEndDateChange}
            min={startDate || getTodayISO()}
          />
        </div>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {!error && days > 0 && (
        <div className="duration-info">
          <span className="duration-badge">
            {days} {days === 1 ? 'día' : 'días'} de estadía
          </span>
        </div>
      )}
    </div>
  );
};

export default DateRangeSelector;

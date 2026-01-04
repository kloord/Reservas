/**
 * Utilidades para manejo de fechas.
 */
import { format, addDays, differenceInDays, isBefore } from 'date-fns';
import { es } from 'date-fns/locale';
/**
 * Parsea una fecha ISO (YYYY-MM-DD) como fecha local
 * evitando el desfase por zona horaria.
 */
export const parseLocalISO = (dateString) => {
  if (!dateString) return null;
  try {
    const [y, m, d] = dateString.split('-').map((n) => parseInt(n, 10));
    return new Date(y, m - 1, d);
  } catch {
    return null;
  }
};

/**
 * Formatea una fecha al formato ISO (YYYY-MM-DD).
 */
export const formatDateToISO = (date) => {
  if (!date) return '';
  return format(date, 'yyyy-MM-dd');
};

/**
 * Formatea una fecha para visualización.
 */
export const formatDateForDisplay = (dateString) => {
  if (!dateString) return '';
  try {
    const date = parseLocalISO(dateString);
    return format(date, 'dd/MM/yyyy', { locale: es });
  } catch {
    return dateString;
  }
};

/**
 * Formatea una fecha de forma larga (ej: "15 de enero de 2025").
 */
export const formatDateLong = (dateString) => {
  if (!dateString) return '';
  try {
    const date = parseLocalISO(dateString);
    return format(date, "dd 'de' MMMM 'de' yyyy", { locale: es });
  } catch {
    return dateString;
  }
};

/**
 * Obtiene la fecha actual en formato ISO.
 */
export const getTodayISO = () => {
  return formatDateToISO(new Date());
};

/**
 * Obtiene la fecha de mañana en formato ISO.
 */
export const getTomorrowISO = () => {
  return formatDateToISO(addDays(new Date(), 1));
};

/**
 * Calcula los días entre dos fechas.
 */
export const daysBetween = (startDateStr, endDateStr) => {
  try {
    const start = parseLocalISO(startDateStr);
    const end = parseLocalISO(endDateStr);
    return differenceInDays(end, start);
  } catch {
    return 0;
  }
};

/**
 * Valida que una fecha de inicio sea anterior a una fecha de fin.
 */
export const isValidDateRange = (startDateStr, endDateStr) => {
  try {
    const start = parseLocalISO(startDateStr);
    const end = parseLocalISO(endDateStr);
    return isBefore(start, end);
  } catch {
    return false;
  }
};

/**
 * Valida que una fecha no esté en el pasado.
 */
export const isNotInPast = (dateStr) => {
  try {
    const date = parseLocalISO(dateStr);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return !isBefore(date, today);
  } catch {
    return false;
  }
};

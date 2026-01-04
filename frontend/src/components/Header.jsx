/**
 * Componente Header - Cabecera de la aplicación.
 */
import './Header.css';
import ReservationSearch from './ReservationSearch';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();
  const isActive = (path) => (location.pathname === path ? 'active' : '');

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-brand">
          <h1>🏡 Sistema de Reservas</h1>
          <p className="header-subtitle">Gestión de Cabañas</p>
        </div>
        <nav className="header-nav">
          <Link className={`nav-link ${isActive('/')}`} to="/">Inicio</Link>
          <Link className={`nav-link ${isActive('/resumen')}`} to="/resumen">Resumen</Link>
        </nav>
        <div className="header-search">
          <ReservationSearch />
        </div>
      </div>
    </header>
  );
};

export default Header;

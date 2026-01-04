/**
 * Componente CabinLayout - Mapa visual de cabañas según orden real.
 * Muestra cada cabaña en su posición con color: verde disponible, rojo ocupada.
 */
import './CabinLayout.css'

// Pairs por columnas según especificación
const columnOnePairs = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
const columnTwoPairs = [[11, 12], [13, 14], [15, 16]]
const columnThreePairs = [[21, 22], [23, 24]]

const CabinLayout = ({ cabinsData, onReserve, onViewDetails, isLoading }) => {
  if (isLoading) {
    return (
      <div className="layout-loading card">
        <div className="spinner" />
        <p>Cargando disponibilidad...</p>
      </div>
    )
  }

  const byId = new Map()
  ;(cabinsData || []).forEach((item) => byId.set(item.cabin.id, item))

  const handleClick = (item, id) => {
    if (!item) return
    if (item.is_available) {
      // Fallback si falta cabin
      const fallbackName = (id >= 21 && id <= 24) ? `Cabaña Express ${id}` : `Cabaña ${id}`
      const cabin = item.cabin || { id, name: fallbackName, capacity: 4 }
      onReserve && onReserve(cabin)
    } else if (onViewDetails) {
      onViewDetails(item.current_reservation)
    }
  }

  return (
    <div className="cabin-layout card">
      <div className="layout-legend">
        <span className="dot available" /> Disponible
        <span className="dot occupied" /> Ocupada
      </div>

      <div className="layout-columns">
        {/* Columna 1 */}
        <div className="layout-column">
          {columnOnePairs.map(([a, b]) => {
            const itemA = byId.get(a)
            const itemB = byId.get(b)
            const clsA = itemA?.is_available ? 'available' : 'occupied'
            const clsB = itemB?.is_available ? 'available' : 'occupied'
            return (
              <div className="pair-row" key={`pair-1-${a}-${b}`}>
                <button className={`cabin-tile ${clsA}`} onClick={() => handleClick(itemA, a)} title={itemA?.is_available ? 'Disponible' : 'Ocupada'}>
                  {a}
                </button>
                <button className={`cabin-tile ${clsB}`} onClick={() => handleClick(itemB, b)} title={itemB?.is_available ? 'Disponible' : 'Ocupada'}>
                  {b}
                </button>
              </div>
            )
          })}
        </div>

        {/* Columna 2 */}
        <div className="layout-column">
          {columnTwoPairs.map(([a, b]) => {
            const itemA = byId.get(a)
            const itemB = byId.get(b)
            const clsA = itemA?.is_available ? 'available' : 'occupied'
            const clsB = itemB?.is_available ? 'available' : 'occupied'
            return (
              <div className="pair-row" key={`pair-2-${a}-${b}`}>
                <button className={`cabin-tile ${clsA}`} onClick={() => handleClick(itemA, a)} title={itemA?.is_available ? 'Disponible' : 'Ocupada'}>
                  {a}
                </button>
                <button className={`cabin-tile ${clsB}`} onClick={() => handleClick(itemB, b)} title={itemB?.is_available ? 'Disponible' : 'Ocupada'}>
                  {b}
                </button>
              </div>
            )
          })}
        </div>

        {/* Columna 3 */}
        <div className="layout-column">
          {columnThreePairs.map(([a, b]) => {
            const itemA = byId.get(a)
            const itemB = byId.get(b)
            const clsA = itemA?.is_available ? 'available' : 'occupied'
            const clsB = itemB?.is_available ? 'available' : 'occupied'
            return (
              <div className="pair-row" key={`pair-3-${a}-${b}`}>
                <button className={`cabin-tile ${clsA}`} onClick={() => handleClick(itemA, a)} title={itemA?.is_available ? 'Disponible' : 'Ocupada'}>
                  {a}
                </button>
                <button className={`cabin-tile ${clsB}`} onClick={() => handleClick(itemB, b)} title={itemB?.is_available ? 'Disponible' : 'Ocupada'}>
                  {b}
                </button>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default CabinLayout

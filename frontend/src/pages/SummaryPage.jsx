import { useEffect, useMemo, useState } from 'react'
import Header from '../components/Header'
import { availabilityService } from '../services/availabilityService'
import { cabinService } from '../services/cabinService'
import { reservationService } from '../services/reservationService'
import './SummaryPage.css'
import ReservationDetailsModal from '../components/ReservationDetailsModal'

// Utilidad para obtener el primer y último día del mes actual en ISO
const getMonthRange = (year, month /* 0-indexed */) => {
  const start = new Date(year, month, 1)
  const end = new Date(year, month + 1, 1)
  const pad = (n) => String(n).padStart(2, '0')
  const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
  return { startISO: iso(start), endISO: iso(end) }
}

const daysInMonth = (year, month) => new Date(year, month + 1, 0).getDate()

const SummaryPage = () => {
  const today = new Date()
  const [year, setYear] = useState(today.getFullYear())
  const [month, setMonth] = useState(today.getMonth()) // 0..11
  const [cabins, setCabins] = useState([])
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedReservation, setSelectedReservation] = useState(null)

  const { startISO, endISO } = useMemo(() => getMonthRange(year, month), [year, month])
  const totalDays = useMemo(() => daysInMonth(year, month), [year, month])

  // Parse YYYY-MM-DD como fecha local (evita desfase por zona horaria)
  const parseLocalISO = (iso) => {
    if (!iso) return null
    const [y, m, d] = iso.split('-').map((n) => parseInt(n, 10))
    return new Date(y, m - 1, d)
  }

  useEffect(() => {
    cabinService.getAll().then(setCabins).catch(() => {})
  }, [])

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError('')
      try {
        // 1) Traer disponibilidad general para lista de cabañas (opcional)
        const res = await availabilityService.checkAvailability(startISO, endISO)
        const byCabin = {}
        for (const item of res.cabins || []) {
          byCabin[item.cabin.id] = {
            cabin: item.cabin,
            is_available: item.is_available,
            current_reservation: item.current_reservation || null,
            reservations: [],
          }
        }
        // 2) Traer todas las reservas que se solapen con el mes
        const reservations = await reservationService.getAll({ start_date: startISO, end_date: endISO })
        for (const r of reservations) {
          if (!byCabin[r.cabin_id]) {
            byCabin[r.cabin_id] = { cabin: cabins.find(c => c.id === r.cabin_id), reservations: [] }
          }
          byCabin[r.cabin_id].reservations = byCabin[r.cabin_id].reservations || []
          byCabin[r.cabin_id].reservations.push(r)
        }
        setData(byCabin)
      } catch (e) {
        setError('Error al cargar el resumen')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [startISO, endISO, cabins])

  const changeMonth = (delta) => {
    const d = new Date(year, month + delta, 1)
    setYear(d.getFullYear())
    setMonth(d.getMonth())
  }

  // Construir matriz de días del mes
  const days = Array.from({ length: totalDays }, (_, i) => i + 1)

  return (
    <div>
      <Header />
      <main className="container">
        <div className="summary-controls card">
          <div className="controls-left">
            <button className="btn btn-secondary" onClick={() => changeMonth(-1)}>
              ◀ Mes anterior
            </button>
            <button className="btn btn-secondary" onClick={() => changeMonth(1)}>
              Mes siguiente ▶
            </button>
          </div>
          <div className="controls-right">
            <h2>
              {new Date(year, month, 1).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' })}
            </h2>
          </div>
        </div>

        {error && <div className="card text-danger">{error}</div>}

        <div className="calendar-grid card">
          <div className="calendar-header" style={{ gridTemplateColumns: `240px repeat(${totalDays}, 1fr)` }}>
            <div className="calendar-cell cabin-col">Cabaña</div>
            {days.map((d) => (
              <div key={d} className="calendar-cell day-col">
                {d}
              </div>
            ))}
          </div>
          <div className="calendar-body">
            {cabins.map((cabin) => (
              <div key={cabin.id} className="calendar-row" style={{ gridTemplateColumns: `240px repeat(${totalDays}, 1fr)` }}>
                <div className="calendar-cell cabin-col cabin-name">{cabin.name}</div>
                {days.map((d) => {
                  const dayDate = new Date(year, month, d)
                  const item = data[cabin.id]
                  let occupied = false
                  let reservationForDay = null
                  let hasCheckin = false
                  let hasCheckout = false
                  if (item && item.reservations && item.reservations.length) {
                    for (const r of item.reservations) {
                      const s = parseLocalISO(r.start_date)
                      const e = parseLocalISO(r.end_date)
                      if (s && +s === +dayDate) {
                        hasCheckin = true
                      }
                      if (e && +e === +dayDate) {
                        hasCheckout = true
                      }
                      if (s && e && dayDate >= s && dayDate < e) {
                        occupied = true
                        reservationForDay = r
                        // seguimos para marcar checkin/checkout si corresponde
                      }
                    }
                  } else if (item && item.current_reservation) {
                    const s = parseLocalISO(item.current_reservation.start_date)
                    const e = parseLocalISO(item.current_reservation.end_date)
                    if (s && +s === +dayDate) hasCheckin = true
                    if (e && +e === +dayDate) hasCheckout = true
                    if (s && e && dayDate >= s && dayDate < e) {
                      occupied = true
                      reservationForDay = item.current_reservation
                    }
                  }

                  // Sábado con cambio de huésped (checkout y checkin mismo día)
                  const isSaturday = dayDate.getDay() === 6 // 0=Domingo, 6=Sábado
                  const turnoverSaturday = isSaturday && hasCheckin && hasCheckout
                  const cellClass = turnoverSaturday
                    ? 'turnover'
                    : occupied
                      ? 'occupied'
                      : 'available'
                  return (
                    <div
                      key={d}
                      className={`calendar-cell day-col ${cellClass} ${(occupied || turnoverSaturday) ? 'occupied-clickable' : ''}`}
                      title={occupied && reservationForDay ? `Reservado por ${reservationForDay.guest_name}` : (turnoverSaturday ? 'Cambio de huésped (sábado)' : '')}
                      onClick={() => (occupied && reservationForDay) ? setSelectedReservation({ r: reservationForDay, cabin }) : null}
                    >
                      {(occupied && reservationForDay) || turnoverSaturday ? (
                        <div className="cell-tooltip">
                          <span className={`tooltip-dot ${turnoverSaturday ? 'dot-blue' : ''}`} />
                          <div className="tooltip-content">
                            {turnoverSaturday && <div className="tooltip-line"><strong>Cambio:</strong> Sábado (checkout/Check-in)</div>}
                            {reservationForDay && (
                              <>
                                <div className="tooltip-line"><strong>Huésped:</strong> {reservationForDay.guest_name}</div>
                                <div className="tooltip-line"><strong>Entrada:</strong> {parseLocalISO(reservationForDay.start_date).toLocaleDateString('es-ES')}</div>
                                <div className="tooltip-line"><strong>Salida:</strong> {parseLocalISO(reservationForDay.end_date).toLocaleDateString('es-ES')}</div>
                              </>
                            )}
                          </div>
                        </div>
                      ) : null}
                    </div>
                  )
                })}
              </div>
            ))}
          </div>
        </div>

        {loading && <p className="text-muted mt-2">Cargando calendario…</p>}

        {selectedReservation && (
          <ReservationDetailsModal
            reservation={selectedReservation.r}
            cabinName={selectedReservation.cabin?.name}
            onClose={() => setSelectedReservation(null)}
          />
        )}
      </main>
    </div>
  )
}

export default SummaryPage

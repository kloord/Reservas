import { useEffect, useMemo, useState } from 'react'
import { reservationService } from '../services/reservationService'
import { cabinService } from '../services/cabinService'
import { formatDateForDisplay } from '../utils/dateUtils'
import ReservationDetailsModal from './ReservationDetailsModal'
import './ReservationSearch.css'

const useDebounced = (value, delay = 300) => {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(t)
  }, [value, delay])
  return debounced
}

const ReservationSearch = () => {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounced(query)
  const [results, setResults] = useState([])
  const [open, setOpen] = useState(false)
  const [cabins, setCabins] = useState([])
  const [selected, setSelected] = useState(null)

  useEffect(() => {
    cabinService.getAll().then(setCabins).catch(() => setCabins([]))
  }, [])

  const byId = useMemo(() => {
    const m = new Map()
    cabins.forEach((c) => m.set(c.id, c))
    return m
  }, [cabins])

  useEffect(() => {
    const run = async () => {
      if (!debouncedQuery || debouncedQuery.trim().length < 2) {
        setResults([])
        setOpen(false)
        return
      }
      try {
        const data = await reservationService.searchByGuestName(debouncedQuery.trim())
        setResults(data)
        setOpen(true)
      } catch (e) {
        setResults([])
        setOpen(false)
      }
    }
    run()
  }, [debouncedQuery])

  const clear = () => {
    setQuery('')
    setResults([])
    setOpen(false)
  }

  return (
    <div className="search-wrap">
      <input
        type="text"
        className="search-input"
        placeholder="Buscar reserva por huésped..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => results.length && setOpen(true)}
      />
      {query && (
        <button className="search-clear" onClick={clear} aria-label="Limpiar">×</button>
      )}

      {open && (
        <div className="search-popover">
          {results.length === 0 ? (
            <div className="empty">Sin resultados</div>
          ) : (
            results.slice(0, 8).map((r) => {
              const cabin = byId.get(r.cabin_id)
              return (
                <button key={r.id} className="result-item" onClick={() => setSelected({ r, cabin })}>
                  <div className="line">
                    <strong>{r.guest_name}</strong>
                    <span className="cabin">{cabin?.name || `Cabaña ${r.cabin_id}`}</span>
                  </div>
                  <div className="line small">
                    <span>{formatDateForDisplay(r.start_date)} → {formatDateForDisplay(r.end_date)}</span>
                  </div>
                </button>
              )
            })
          )}
        </div>
      )}

      {selected && (
        <ReservationDetailsModal reservation={selected.r} cabinName={selected.cabin?.name} onClose={() => setSelected(null)} />
      )}
    </div>
  )
}

export default ReservationSearch

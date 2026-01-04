import { useEffect, useState } from 'react'
import Header from './components/Header'
import DateRangeSelector from './components/DateRangeSelector'
import CabinLayout from './components/CabinLayout'
import ReservationModal from './components/ReservationModal'
import { availabilityService } from './services/availabilityService'
import { cabinService } from './services/cabinService'
import './index.css'

function App() {
  const [dateRange, setDateRange] = useState({ startDate: '', endDate: '' })
  const [availabilityData, setAvailabilityData] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedCabin, setSelectedCabin] = useState(null)
  const [selectedReservation, setSelectedReservation] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [cabins, setCabins] = useState([])

  useEffect(() => {
    // Cargar cabañas para tener nombres y capacidades actualizados
    const fetchCabins = async () => {
      try {
        const data = await cabinService.getAll()
        setCabins(data)
      } catch (err) {
        console.error('Error al cargar cabañas', err)
      }
    }

    fetchCabins()
  }, [])

  const loadAvailability = async (startDate, endDate) => {
    setLoading(true)
    setError('')
    try {
      const result = await availabilityService.checkAvailability(startDate, endDate)
      // Normalizar estructura para CabinGrid
      const normalized = result.cabins?.map((c) => ({
        cabin: c.cabin,
        is_available: c.is_available,
        current_reservation: c.current_reservation || null,
      })) || []
      setAvailabilityData(normalized)
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Error al cargar disponibilidad'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleDateChange = ({ startDate, endDate }) => {
    setDateRange({ startDate, endDate })
    loadAvailability(startDate, endDate)
  }

  const openReservationModal = (cabin) => {
    setSelectedCabin(cabin)
    setSelectedReservation(null)
    setIsModalOpen(true)
  }

  const openDetailsModal = (reservation) => {
    // Necesitamos la cabaña completa para capacidad/nombre
    const cabin = cabins.find((c) => c.id === reservation.cabin_id) || {
      id: reservation.cabin_id,
      name: `Cabaña ${reservation.cabin_id}`,
      capacity: 4,
    }
    setSelectedCabin(cabin)
    setSelectedReservation(reservation)
    setIsModalOpen(true)
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setSelectedCabin(null)
    setSelectedReservation(null)
  }

  const handleReservationSuccess = () => {
    if (dateRange.startDate && dateRange.endDate) {
      loadAvailability(dateRange.startDate, dateRange.endDate)
    }
  }

  return (
    <div>
      <Header />
      <main className="container">
        <DateRangeSelector onDateChange={handleDateChange} />

        {error && (
          <div className="card" style={{ borderLeft: '4px solid var(--danger-color)' }}>
            <p className="text-danger">{error}</p>
          </div>
        )}

        <CabinLayout
          cabinsData={availabilityData}
          onReserve={openReservationModal}
          onViewDetails={openDetailsModal}
          isLoading={loading}
        />
      </main>

      <ReservationModal
        isOpen={isModalOpen}
        onClose={closeModal}
        cabin={selectedCabin}
        startDate={dateRange.startDate}
        endDate={dateRange.endDate}
        existingReservation={selectedReservation}
        onSuccess={handleReservationSuccess}
      />
    </div>
  )
}

export default App

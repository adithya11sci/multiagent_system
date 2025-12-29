import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import TrainDelay from './pages/TrainDelay'
import PassengerQuery from './pages/PassengerQuery'
import CrowdPrediction from './pages/CrowdPrediction'
import Alerts from './pages/Alerts'
import Agents from './pages/Agents'

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="train-delay" element={<TrainDelay />} />
          <Route path="passenger-query" element={<PassengerQuery />} />
          <Route path="crowd-prediction" element={<CrowdPrediction />} />
          <Route path="alerts" element={<Alerts />} />
          <Route path="agents" element={<Agents />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App

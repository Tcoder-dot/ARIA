import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import RunThread from './pages/RunThread'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/run/:runId" element={<RunThread />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App


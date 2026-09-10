import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import History from './pages/History'
import Settings from './pages/Settings'

function App() {
  const [currentPage, setCurrentPage] = useState('home')

  return (
    <div className="app">
      <Navbar
        currentPage={currentPage}
        onNavigate={setCurrentPage}
      />

      {currentPage === 'home' && <Home />}
      {currentPage === 'history' && <History />}
      {currentPage === 'settings' && <Settings />}

      <footer>
        <p>PolyVoice · Multilingual Voice Communication</p>
      </footer>
    </div>
  )
}

export default App
import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'

function App() {
  return (
    <div className="app">
      <Navbar />

      <Home />

      <footer>
        <p>PolyVoice · Multilingual Voice Communication</p>
      </footer>
    </div>
  )
}

export default App
// import { useState } from 'react'
// import './App.css'
// import Navbar from './components/Navbar'
// import Home from './pages/Home'
// import History from './pages/History'
// import Settings from './pages/Settings'
// import Login from './pages/Login'
// import Signup from './pages/Signup'

// function App() {
//   const [currentPage, setCurrentPage] = useState('home')

//   return (
//     <div className="app">
//       <Navbar
//         currentPage={currentPage}
//         onNavigate={setCurrentPage}
//       />

//       {currentPage === 'home' && <Home />}
//       {currentPage === 'history' && <History />}
//       {currentPage === 'settings' && <Settings />}
//       {currentPage === 'login' && <Login />}
//       {currentPage === 'signup' && <Signup />}

//       <footer>
//         <p>PolyVoice · Multilingual Voice Communication</p>
//       </footer>
//     </div>
//   )
// }

// export default App

import { useState, useEffect } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import History from './pages/History'
import Settings from './pages/Settings'
import Login from './pages/Login'
import Signup from './pages/Signup'

function App() {
  const [currentPage, setCurrentPage] = useState('login')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [checkingAuth, setCheckingAuth] = useState(true)

  // Verify token whenever the application loads
  useEffect(() => {
    const verifyToken = async () => {
      const token = sessionStorage.getItem('access_token')

      if (!token) {
        setIsAuthenticated(false)
        setCurrentPage('login')
        setCheckingAuth(false)
        return
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/auth/me', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          throw new Error('Invalid token')
        }

        const user = await response.json()

        sessionStorage.setItem('user', JSON.stringify(user))

        setIsAuthenticated(true)
        setCurrentPage('home')

      } catch (error) {
        sessionStorage.removeItem('access_token')
        sessionStorage.removeItem('user')

        setIsAuthenticated(false)
        setCurrentPage('login')
      } finally {
        setCheckingAuth(false)
      }
    }

    verifyToken()
  }, [])

  // Login to Signup navigation
  useEffect(() => {
    const openSignup = () => {
      setCurrentPage('signup')
    }

    window.addEventListener('open-signup', openSignup)

    return () => {
      window.removeEventListener('open-signup', openSignup)
    }
  }, [])

    // Signup to Login navigation
  useEffect(() => {
    const openLogin = () => {
      setCurrentPage('login')
    }

    window.addEventListener('open-login', openLogin)

    return () => {
      window.removeEventListener('open-login', openLogin)
    }
  }, [])
  // Handle successful login
  const handleLoginSuccess = () => {
    setIsAuthenticated(true)
    setCurrentPage('home')
  }

  // Handle logout
  const handleLogout = () => {
    sessionStorage.removeItem('access_token')
    sessionStorage.removeItem('user')

    setIsAuthenticated(false)
    setCurrentPage('login')
  }

  // Navigation protection
  const navigate = (page) => {
    const protectedPages = ['home', 'history', 'settings']

    if (protectedPages.includes(page) && !isAuthenticated) {
      setCurrentPage('login')
      return
    }

    setCurrentPage(page)
  }

  if (checkingAuth) {
    return <div>Checking authentication...</div>
  }

  return (
    <div className="app">

      {isAuthenticated && (
        <Navbar
          currentPage={currentPage}
          onNavigate={navigate}
          onLogout={handleLogout}
        />
      )}

      {currentPage === 'home' && isAuthenticated && <Home />}

      {currentPage === 'history' && isAuthenticated && <History />}

      {currentPage === 'settings' && isAuthenticated && <Settings />}

      {currentPage === 'login' && (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}

      {currentPage === 'signup' && (
  <Signup onSignupSuccess={handleLoginSuccess} />
)}

      <footer>
        <p>PolyVoice · Multilingual Voice Translation</p>
      </footer>

    </div>
  )
}

export default App
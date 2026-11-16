// function Login() {
//   return (
//     <main className="auth-page">
//       <section className="auth-card">
//         <p className="tagline">WELCOME BACK</p>

//         <h1>
//           Sign in to
//           <br />
//           <span>VOCAL-X.</span>
//         </h1>

//         <p className="auth-description">
//           Continue your multilingual voice translation experience.
//         </p>

//         <form className="auth-form">
//           <div className="form-group">
//             <label htmlFor="email">Email</label>
//             <input
//               id="email"
//               type="email"
//               placeholder="Enter your email"
//             />
//           </div>

//           <div className="form-group">
//             <label htmlFor="password">Password</label>
//             <input
//               id="password"
//               type="password"
//               placeholder="Enter your password"
//             />
//           </div>

//           <button type="submit" className="auth-btn">
//             Log in
//             <span>→</span>
//           </button>
//         </form>

//         <p className="auth-footer">
//           Don't have an account?{' '}
//           <a href="#signup">Sign up</a>
//         </p>
//       </section>
//     </main>
//   )
// }

// export default Login

import { useState } from 'react'

function Login({ onLoginSuccess }) {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setMessage('')
    setLoading(true)

    const formData = new FormData(e.currentTarget)

    const loginData = {
      email: formData.get('email'),
      password: formData.get('password'),
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed')
      }

      sessionStorage.setItem('access_token', data.access_token)
      sessionStorage.setItem('user', JSON.stringify(data.user))

      onLoginSuccess()

    } catch (error) {
      setMessage(error.message || 'Unable to connect to the server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <p className="tagline">WELCOME BACK</p>

        <h1>
          Sign in to
          <br />
          <span>VOCAL-X.</span>
        </h1>

        <p className="auth-description">
          Continue your multilingual voice translation experience.
        </p>

        <form className="auth-form" onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? 'Logging in...' : 'Log in'}
            <span>→</span>
          </button>
        </form>

        {message && (
          <p style={{ color: 'red', marginTop: '15px' }}>
            {message}
          </p>
        )}

        <p className="auth-footer">
  Don't have an account?{' '}
  <button type="button" onClick={() => window.dispatchEvent(new Event('open-signup'))}>
    Sign up
  </button>
</p>
      </section>
    </main>
  )
}

export default Login
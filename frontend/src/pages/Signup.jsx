// function Signup() {
//   return (
//     <main className="auth-page">
//       <section className="auth-card">
//         <p className="tagline">GET STARTED</p>

//         <h1>
//           Create your
//           <br />
//           <span>VOCAL-X account.</span>
//         </h1>

//         <p className="auth-description">
//           Create an account to use multilingual voice translation.
//         </p>

//         <form className="auth-form">
//           <div className="form-group">
//             <label htmlFor="name">Name</label>
//             <input
//               id="name"
//               type="text"
//               placeholder="Enter your name"
//             />
//           </div>

//           <div className="form-group">
//             <label htmlFor="signup-email">Email</label>
//             <input
//               id="signup-email"
//               type="email"
//               placeholder="Enter your email"
//             />
//           </div>

//           <div className="form-group">
//             <label htmlFor="signup-password">Password</label>
//             <input
//               id="signup-password"
//               type="password"
//               placeholder="Create a password"
//             />
//           </div>

//           <button type="submit" className="auth-btn">
//             Sign up
//             <span>→</span>
//           </button>
//         </form>

//         <p className="auth-footer">
//           Already have an account?{' '}
//           <a href="#login">Log in</a>
//         </p>
//       </section>
//     </main>
//   )
// }

// export default Signup

import { useState } from 'react'

function Signup({ onSignupSuccess }) {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSignup = async (e) => {
    e.preventDefault()

    setMessage('')
    setLoading(true)

    const formData = new FormData(e.currentTarget)

    const userData = {
      full_name: formData.get('full_name'),
      email: formData.get('email'),
      password: formData.get('password'),
    }

    try {
      // Step 1: Create account
      const signupResponse = await fetch(
        'http://127.0.0.1:8000/api/auth/signup',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        }
      )

      const signupData = await signupResponse.json()

      if (!signupResponse.ok) {
        throw new Error(signupData.detail || 'Signup failed')
      }

      // Step 2: Automatically log in the new user
      const loginResponse = await fetch(
        'http://127.0.0.1:8000/api/auth/login',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: userData.email,
            password: userData.password,
          }),
        }
      )

      const loginData = await loginResponse.json()

      if (!loginResponse.ok) {
        throw new Error(
          'Account created successfully. Please log in manually.'
        )
      }

      // Step 3: Store authentication details
      sessionStorage.setItem('access_token', loginData.access_token)
      sessionStorage.setItem('user', JSON.stringify(loginData.user))

      // Step 4: Redirect to Home
      onSignupSuccess()

    } catch (error) {
      setMessage(error.message || 'Unable to connect to the server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <p className="tagline">GET STARTED</p>

        <h1>
          Create your
          <br />
          <span>VOCAL-X account.</span>
        </h1>

        <p className="auth-description">
          Create an account to use multilingual voice translation.
        </p>

        <form className="auth-form" onSubmit={handleSignup}>
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="full_name"
              type="text"
              placeholder="Enter your name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="signup-email">Email</label>
            <input
              id="signup-email"
              name="email"
              type="email"
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="signup-password">Password</label>
            <input
              id="signup-password"
              name="password"
              type="password"
              placeholder="Create a password"
              minLength={8}
              required
            />
          </div>

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign up'}
            <span>→</span>
          </button>
        </form>

        {message && (
          <p style={{ color: 'red', marginTop: '15px' }}>
            {message}
          </p>
        )}

        <p className="auth-footer">
          Already have an account?{' '}
          <button
            type="button"
            onClick={() => window.dispatchEvent(new Event('open-login'))}
          >
            Log in
          </button>
        </p>
      </section>
    </main>
  )
}

export default Signup
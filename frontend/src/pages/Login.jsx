function Login() {
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

        <form className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" className="auth-btn">
            Log in
            <span>→</span>
          </button>
        </form>

        <p className="auth-footer">
          Don't have an account?{' '}
          <a href="#signup">Sign up</a>
        </p>
      </section>
    </main>
  )
}

export default Login
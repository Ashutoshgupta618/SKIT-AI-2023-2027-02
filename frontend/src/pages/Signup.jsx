function Signup() {
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

        <form className="auth-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              type="text"
              placeholder="Enter your name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="signup-email">Email</label>
            <input
              id="signup-email"
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="signup-password">Password</label>
            <input
              id="signup-password"
              type="password"
              placeholder="Create a password"
            />
          </div>

          <button type="submit" className="auth-btn">
            Sign up
            <span>→</span>
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{' '}
          <a href="#login">Log in</a>
        </p>
      </section>
    </main>
  )
}

export default Signup
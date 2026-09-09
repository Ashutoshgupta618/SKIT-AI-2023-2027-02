function Navbar() {
  return (
    <header className="navbar">
      <div className="logo">PolyVoice</div>

      <nav>
        <a href="#translate">Translate</a>
        <a href="#history">History</a>
        <a href="#settings">Settings</a>
      </nav>

      <div className="account">
        <button className="login-btn">Log in</button>
        <button className="signup-btn">Sign up</button>
      </div>
    </header>
  )
}

export default Navbar
function Navbar({ currentPage, onNavigate }) {
  return (
    <header className="navbar">
      <div className="logo">VOCAL-X</div>

      <nav>
        <a
          href="#translate"
          onClick={(e) => {
            e.preventDefault()
            onNavigate('home')
          }}
        >
          Translate
        </a>

        <a
          href="#history"
          onClick={(e) => {
            e.preventDefault()
            onNavigate('history')
          }}
        >
          History
        </a>

        <a
  href="#settings"
  onClick={(e) => {
    e.preventDefault()
    onNavigate('settings')
  }}
>
  Settings
</a>
      </nav>

      <div className="account">
        <button className="login-btn">Log in</button>
        <button className="signup-btn">Sign up</button>
      </div>
    </header>
  )
}

export default Navbar
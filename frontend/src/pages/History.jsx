function History() {
  return (
    <main className="page-container">
      <section className="page-header">
        <p className="tagline">YOUR ACTIVITY</p>

        <h1>
          Translation
          <br />
          <span>history.</span>
        </h1>

        <p className="page-description">
          Your previous voice translations will appear here.
        </p>
      </section>

      <section className="history-container">
        <div className="history-empty">
          <div className="history-icon">◷</div>

          <h2>No translations yet</h2>

          <p>
            Your completed translations will be saved here
            once history functionality is connected.
          </p>

          <a href="#translate" className="history-action">
            Start translating →
          </a>
        </div>
      </section>
    </main>
  )
}

export default History
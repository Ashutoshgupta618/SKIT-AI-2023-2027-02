function Settings() {
  return (
    <main className="page-container">
      <section className="page-header">
        <p className="tagline">PREFERENCES</p>

        <h1>
          Your
          <br />
          <span>settings.</span>
        </h1>

        <p className="page-description">
          Manage your language, audio and application preferences.
        </p>
      </section>

      <section className="settings-container">
        <div className="settings-card">
          <div className="setting-item">
            <div>
              <h3>Default source language</h3>
              <p>Language used when you start a new translation.</p>
            </div>

            <select defaultValue="English">
              <option>English</option>
              <option>Hindi</option>
              <option>Bengali</option>
              <option>Gujarati</option>
              <option>Kannada</option>
              <option>Malayalam</option>
              <option>Marathi</option>
              <option>Odia</option>
              <option>Punjabi</option>
              <option>Tamil</option>
              <option>Telugu</option>
            </select>
          </div>

          <div className="setting-item">
            <div>
              <h3>Default target language</h3>
              <p>Language used for translated output.</p>
            </div>

            <select defaultValue="Hindi">
              <option>English</option>
              <option>Hindi</option>
              <option>Bengali</option>
              <option>Gujarati</option>
              <option>Kannada</option>
              <option>Malayalam</option>
              <option>Marathi</option>
              <option>Odia</option>
              <option>Punjabi</option>
              <option>Tamil</option>
              <option>Telugu</option>
            </select>
          </div>

          <div className="setting-item">
            <div>
              <h3>Auto-play translation</h3>
              <p>Automatically play translated audio when available.</p>
            </div>

            <button className="toggle-btn" type="button">
              Off
            </button>
          </div>

          <div className="setting-item">
            <div>
              <h3>Save translation history</h3>
              <p>Keep completed translations available in your history.</p>
            </div>

            <button className="toggle-btn active" type="button">
              On
            </button>
          </div>
        </div>
      </section>
    </main>
  )
}

export default Settings
import { useState } from 'react'
import './App.css'

function App() {
  const [isRecording, setIsRecording] = useState(false)

  const [recognizedText, setRecognizedText] = useState('')

  const handleMicClick = () => {

    setIsRecording((prev) => !prev)

    if (!isRecording) {

      setRecognizedText('Listening...')

    } else {

      setRecognizedText('Your recognized speech will appear here...')

    }

  }
  return (
    <div className="app">
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

      <main>
        <section className="hero-section">
          <p className="tagline">SPEAK. TRANSLATE. CONNECT.</p>

          <h1>
            Your voice,
            <br />
            <span>without borders.</span>
          </h1>

          <p className="hero-text">
            Speak naturally in your language and let PolyVoice
            translate your voice into another language.
          </p>
        </section>

        <section className="translator" id="translate">
          <div className="language-row">
            <div className="language-select">
              <label>From</label>
              <select defaultValue="English">
                <option>English</option>
                <option>Hindi</option>
                <option>Spanish</option>
                <option>French</option>
                <option>German</option>
                <option>Japanese</option>
              </select>
            </div>

            <button className="swap-btn">⇄</button>

            <div className="language-select">
              <label>To</label>
              <select defaultValue="Hindi">
                <option>Hindi</option>
                <option>English</option>
                <option>Spanish</option>
                <option>French</option>
                <option>German</option>
                <option>Japanese</option>
              </select>
            </div>
          </div>

          <div className="translation-grid">
            <div className="translation-card">
              <div className="card-header">
                <span>YOUR VOICE</span>
                <span className="status">● Ready</span>
              </div>

              <div className="voice-area">
                <button
                  className={`mic-btn ${isRecording ? 'recording' : ''}`}
                   onClick={handleMicClick} >🎙️
                </button>
                <p>{isRecording ? 'Listening...' : 'Tap to speak'}</p>
                <small>Your speech will appear here</small>
              </div>

              <div className="text-output">
                 {recognizedText || 'Your recognized speech will appear here...'}
              </div> 
            </div>

            <div className="translation-card">
              <div className="card-header">
                <span>TRANSLATION</span>
                <span className="status">Ready</span>
              </div>

              <div className="translated-text">
                <p>Your translated text will appear here...</p>
              </div>

              <button className="audio-btn">
                🔊 Play translated audio
              </button>
            </div>
          </div>

          <button className="translate-btn">
            Translate Voice
            <span>→</span>
          </button>
        </section>
      </main>

      <footer>
        <p>PolyVoice · Multilingual Voice Communication</p>
      </footer>
    </div>
  )
}

export default App
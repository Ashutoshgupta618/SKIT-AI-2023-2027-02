import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import LanguageSelector from './components/LanguageSelector'
function App() {
  const [isRecording, setIsRecording] = useState(false)

  const [recognizedText, setRecognizedText] = useState('')
  const languages = [
  'English',
  'Hindi',
  'Bengali',
  'Gujarati',
  'Kannada',
  'Malayalam',
  'Marathi',
  'Odia',
  'Punjabi',
  'Tamil',
  'Telugu',
]

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
       <Navbar />

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
           <LanguageSelector
             label="From"
             value="English"
             onChange={() => {}}
             languages={languages}
           />

            <button className="swap-btn">⇄</button>

            <LanguageSelector
             label="To"
             value="Hindi"
             onChange={() => {}}
              languages={languages}
            />
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
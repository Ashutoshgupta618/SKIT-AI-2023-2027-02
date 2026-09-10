import { useState } from 'react'
import LanguageSelector from '../components/LanguageSelector'
import VoiceRecorder from '../components/VoiceRecorder'
import TranslationBox from '../components/TranslationBox'

function Home() {
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

  return (
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

            <VoiceRecorder
              onRecordingComplete={() => {
                setRecognizedText(
                  'Recording completed. Ready for speech recognition.',
                )
              }}
            />

            <div className="text-output">
              {recognizedText || 'Your recognized speech will appear here...'}
            </div>
          </div>

          <TranslationBox translatedText="" />
        </div>

        <button className="translate-btn">
          Translate Voice
          <span>→</span>
        </button>
      </section>
    </main>
  )
}

export default Home
// import { useState } from 'react'
// import LanguageSelector from '../components/LanguageSelector'
// import VoiceRecorder from '../components/VoiceRecorder'
// import TranslationBox from '../components/TranslationBox'

// function Home() {
//   const [recognizedText, setRecognizedText] = useState('')

//   const languages = [
//     'English',
//     'Hindi',
//     'Bengali',
//     'Gujarati',
//     'Kannada',
//     'Malayalam',
//     'Marathi',
//     'Odia',
//     'Punjabi',
//     'Tamil',
//     'Telugu',
//   ]

//   return (
//     <main>
//       <section className="hero-section">
//         <p className="tagline">SPEAK. TRANSLATE. CONNECT.</p>

//         <h1>
//           Your voice,
//           <br />
//           <span>without borders.</span>
//         </h1>

//         <p className="hero-text">
//           Speak naturally in your language and let PolyVoice
//           translate your voice into another language.
//         </p>
//       </section>

//       <section className="translator" id="translate">
//         <div className="language-row">
//           <LanguageSelector
//             label="From"
//             value="English"
//             onChange={() => {}}
//             languages={languages}
//           />

//           <button className="swap-btn">⇄</button>

//           <LanguageSelector
//             label="To"
//             value="Hindi"
//             onChange={() => {}}
//             languages={languages}
//           />
//         </div>

//         <div className="translation-grid">
//           <div className="translation-card">
//             <div className="card-header">
//               <span>YOUR VOICE</span>
//               <span className="status">● Ready</span>
//             </div>

//             <VoiceRecorder
//               onRecordingComplete={() => {
//                 setRecognizedText(
//                   'Recording completed. Ready for speech recognition.',
//                 )
//               }}
//             />

//             <div className="text-output">
//               {recognizedText || 'Your recognized speech will appear here...'}
//             </div>
//           </div>

//           <TranslationBox translatedText="" />
//         </div>

//         <button className="translate-btn">
//           Translate Voice
//           <span>→</span>
//         </button>
//       </section>
//     </main>
//   )
// }

// export default Home

import { useState, useEffect } from 'react'
import LanguageSelector from '../components/LanguageSelector'
import VoiceRecorder from '../components/VoiceRecorder'
import TranslationBox from '../components/TranslationBox'

function Home() {
  const [recognizedText, setRecognizedText] = useState('')
  const [translatedText, setTranslatedText] = useState('')
  const [audioUrl, setAudioUrl] = useState('')

  const [sourceLanguage, setSourceLanguage] = useState('English')
  const [targetLanguage, setTargetLanguage] = useState('Hindi')

  const [loading, setLoading] = useState(false)
  const [translating, setTranslating] = useState(false)
  const [audioLoading, setAudioLoading] = useState(false)
  const [error, setError] = useState('')

  const languages = ['English', 'Hindi', 'Bengali', 'Gujarati']

  useEffect(() => {
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl)
      }
    }
  }, [audioUrl])

  const generateAudio = async (text, language) => {
    setAudioLoading(true)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/speech/generate',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text,
            language,
          }),
        }
      )

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Audio generation failed')
      }

      const audioBlob = await response.blob()
      const newAudioUrl = URL.createObjectURL(audioBlob)

      setAudioUrl((previousUrl) => {
        if (previousUrl) {
          URL.revokeObjectURL(previousUrl)
        }

        return newAudioUrl
      })

    } catch (err) {
      setError(err.message || 'Audio generation failed')
    } finally {
      setAudioLoading(false)
    }
  }

  const handleTranslation = async (
    text = recognizedText,
    source = sourceLanguage,
    target = targetLanguage
  ) => {
    if (!text.trim()) return

    setTranslating(true)
    setError('')
    setTranslatedText('')
    setAudioUrl('')

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/translation/translate',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text,
            source_language: source,
            target_language: target,
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Translation failed')
      }

      setTranslatedText(data.translated_text)

      await generateAudio(data.translated_text, target)

    } catch (err) {
      setError(err.message || 'Translation failed')
    } finally {
      setTranslating(false)
    }
  }

  const handleRecordingComplete = async (audioBlob) => {
    if (!audioBlob) return

    setLoading(true)
    setError('')
    setRecognizedText('')
    setTranslatedText('')
    setAudioUrl('')

    try {
      const formData = new FormData()

      const extension = audioBlob.type.includes('mp4') ? 'm4a' : 'webm'

      formData.append('audio', audioBlob, `recording.${extension}`)
      formData.append('language', sourceLanguage)

      const response = await fetch(
        'http://127.0.0.1:8000/api/voice/transcribe',
        {
          method: 'POST',
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Speech recognition failed')
      }

      const text = data.recognized_text

      setRecognizedText(text)

      await handleTranslation(text, sourceLanguage, targetLanguage)

    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const handleSwap = () => {
    setSourceLanguage(targetLanguage)
    setTargetLanguage(sourceLanguage)
    setTranslatedText('')
    setAudioUrl('')
  }

  const handleSourceChange = (language) => {
    setSourceLanguage(language)
    setTranslatedText('')
    setAudioUrl('')
  }

  const handleTargetChange = (language) => {
    setTargetLanguage(language)
    setTranslatedText('')
    setAudioUrl('')
  }

  return (
    <main>
      <section className="hero-section">
        <p className="tagline">SPEAK. TRANSLATE. CONNECT.</p>

        <h1>
          Your voice,<br />
          <span>without borders.</span>
        </h1>

        <p className="hero-text">
          Speak naturally in your language and let Vocal-X
          translate your voice into another language.
        </p>
      </section>

      <section className="translator" id="translate">

        <div className="language-row">
          <LanguageSelector
            label="From"
            value={sourceLanguage}
            onChange={handleSourceChange}
            languages={languages}
          />

          <button className="swap-btn" onClick={handleSwap}>
            ⇄
          </button>

          <LanguageSelector
            label="To"
            value={targetLanguage}
            onChange={handleTargetChange}
            languages={languages}
          />
        </div>

        <div className="translation-grid">

          <div className="translation-card">
            <div className="card-header">
              <span>YOUR VOICE</span>
              <span className="status">
                ● {loading ? 'Processing' : 'Ready'}
              </span>
            </div>

            <VoiceRecorder
              onRecordingComplete={handleRecordingComplete}
            />

            <div className="text-output">
              {loading
                ? 'Recognizing your speech...'
                : recognizedText || 'Your recognized speech will appear here...'}
            </div>
          </div>

          <TranslationBox
            translatedText={translatedText}
            audioUrl={audioUrl}
            audioLoading={audioLoading}
          />

        </div>

        {error && (
          <p style={{ color: 'red', marginTop: '15px' }}>
            {error}
          </p>
        )}

        <button
          className="translate-btn"
          onClick={() => handleTranslation()}
          disabled={!recognizedText || loading || translating || audioLoading}
        >
          {translating
            ? 'Translating...'
            : audioLoading
              ? 'Generating audio...'
              : 'Translate'}
          <span> →</span>
        </button>

      </section>
    </main>
  )
}

export default Home
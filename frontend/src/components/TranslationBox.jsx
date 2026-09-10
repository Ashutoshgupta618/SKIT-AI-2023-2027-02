function TranslationBox({ translatedText }) {
  return (
    <div className="translation-card">
      <div className="card-header">
        <span>TRANSLATION</span>
        <span className="status">Ready</span>
      </div>

      <div className="translated-text">
        <p>
          {translatedText || 'Your translated text will appear here...'}
        </p>
      </div>
    </div>
  )
}

export default TranslationBox
function LanguageSelector({ label, value, onChange, languages }) {
  return (
    <div className="language-select">
      <label>{label}</label>

      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {languages.map((language) => (
          <option key={language} value={language}>
            {language}
          </option>
        ))}
      </select>
    </div>
  )
}

export default LanguageSelector
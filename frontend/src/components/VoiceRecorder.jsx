import { useState } from 'react'

function VoiceRecorder({ onRecordingComplete }) {
  const [isRecording, setIsRecording] = useState(false)

  const handleRecording = () => {
    if (!isRecording) {
      setIsRecording(true)
      return
    }

    setIsRecording(false)

    if (onRecordingComplete) {
      onRecordingComplete()
    }
  }

  return (
    <div className="voice-recorder">
      <button
        className={`mic-button ${isRecording ? 'recording' : ''}`}
        onClick={handleRecording}
        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
      >
        {isRecording ? '⏹' : '🎙️'}
      </button>

      <p>
        {isRecording
          ? 'Listening... Click to stop'
          : 'Click the microphone to speak'}
      </p>
    </div>
  )
}

export default VoiceRecorder
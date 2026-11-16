// import { useState } from 'react'

// function VoiceRecorder({ onRecordingComplete }) {
//   const [isRecording, setIsRecording] = useState(false)

//   const handleRecording = () => {
//     if (!isRecording) {
//       setIsRecording(true)
//       return
//     }

//     setIsRecording(false)

//     if (onRecordingComplete) {
//       onRecordingComplete()
//     }
//   }

//   return (
//     <div className="voice-recorder">
//       <button
//         className={`mic-button ${isRecording ? 'recording' : ''}`}
//         onClick={handleRecording}
//         aria-label={isRecording ? 'Stop recording' : 'Start recording'}
//       >
//         {isRecording ? '⏹' : '🎙️'}
//       </button>

//       <p>
//         {isRecording
//           ? 'Listening... Click to stop'
//           : 'Click the microphone to speak'}
//       </p>
//     </div>
//   )
// }

// export default VoiceRecorder

import { useState, useRef } from 'react'

function VoiceRecorder({ onRecordingComplete }) {
  const [isRecording, setIsRecording] = useState(false)
  const [isStarting, setIsStarting] = useState(false)
  const [error, setError] = useState('')

  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const streamRef = useRef(null)

  const startRecording = async () => {
    try {
      setError('')
      setIsStarting(true)

      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      })

      streamRef.current = stream
      audioChunksRef.current = []

      // Create audio recorder
      const recorder = new MediaRecorder(stream)

      mediaRecorderRef.current = recorder

      // Collect recorded audio
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      // When recording stops
      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: recorder.mimeType || 'audio/webm',
        })

        // Stop microphone tracks
        stream.getTracks().forEach((track) => track.stop())

        streamRef.current = null

        // Send audio to parent component
        if (onRecordingComplete) {
          onRecordingComplete(audioBlob)
        }
      }

      recorder.start()

      setIsRecording(true)

    } catch (error) {
      console.error('Microphone error:', error)

      setError(
        'Unable to access microphone. Please allow microphone permission.'
      )
    } finally {
      setIsStarting(false)
    }
  }

  const stopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === 'recording'
    ) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleRecording = () => {
    if (isRecording) {
      stopRecording()
    } else {
      startRecording()
    }
  }

  return (
    <div className="voice-recorder">

      <button
        className={`mic-button ${isRecording ? 'recording' : ''}`}
        onClick={handleRecording}
        disabled={isStarting}
        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
      >
        {isStarting ? '...' : isRecording ? '⏹' : '🎙️'}
      </button>

      <p>
        {isStarting
          ? 'Starting microphone...'
          : isRecording
            ? 'Listening... Click to stop'
            : 'Click the microphone to speak'}
      </p>

      {error && (
        <p style={{ color: 'red', fontSize: '14px' }}>
          {error}
        </p>
      )}

    </div>
  )
}

export default VoiceRecorder
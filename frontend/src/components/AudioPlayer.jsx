// function AudioPlayer() {
//   return (
//     <button className="audio-btn">
//       🔊 Play translated audio
//     </button>
//   )
// }

// export default AudioPlayer

function AudioPlayer({ audioUrl, loading }) {
  if (loading) {
    return (
      <button className="audio-btn" disabled>
        Generating audio...
      </button>
    )
  }

  if (!audioUrl) {
    return (
      <button className="audio-btn" disabled>
        🔊 Audio will appear here
      </button>
    )
  }

  return (
    <div className="audio-player">
      <audio controls src={audioUrl}>
        Your browser does not support audio playback.
      </audio>
    </div>
  )
}

export default AudioPlayer
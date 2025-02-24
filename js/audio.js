const audioContext = new window.AudioContext();

// Speak a message aloud using browser SpeechSynthesisUtterance
export const say = (message) => {
  if (message) {
    let utterance = new SpeechSynthesisUtterance(message);
    window.speechSynthesis.speak(utterance);
  }
};

export function play_tone(
  frequency = 440,
  duration_ms = 1000,
  volume = 0.1,
  type = "sine",
  message = null
) {
  // Create an OscillatorNode
  const oscillator = audioContext.createOscillator();

  // Create a gain node
  const gain = audioContext.createGain();

  // Set the volume
  gain.gain.value = volume;

  // Set the type of the oscillator
  oscillator.type = type;

  // Set the frequency of the oscillator
  oscillator.frequency.value = frequency;

  // Connect the gain function
  oscillator.connect(gain);

  // Connect the oscillator to the audio context's destination (the speakers)
  gain.connect(audioContext.destination);

  // Start the oscillator immediately
  oscillator.start();

  // Set the gain envelope
  gain.gain.exponentialRampToValueAtTime(
    0.00001,
    audioContext.currentTime + duration_ms / 1000
  );

  // Stop the oscillator after the specified duration
  setTimeout(() => {
    oscillator.stop();
    if (message)
      setTimeout(() => {
        say(message);
      }, 100);
  }, duration_ms);
}

export function play_success(msg = null) {
  play_tone(500, 5, 0.05, "sine", msg);
}

export function play_error(msg = null) {
  play_tone(50, 400, 0.1, "sawtooth", msg);
}

export default { say, play_tone, play_success, play_error };

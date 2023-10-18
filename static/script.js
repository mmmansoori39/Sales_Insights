<script>
    let recognition;

    function toggleVoiceCommand() {
      if (!recognition) {
        recognition = new webkitSpeechRecognition || SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.onresult = handleSpeechResult;
        recognition.start();

        document.getElementById('voiceCommandButton').textContent = 'Disable Voice Command';

        // Add event listeners for various events
        document.addEventListener('click', handleVoiceCommand);
        document.addEventListener('keydown', handleVoiceCommand);
        document.addEventListener('change', handleVoiceCommand);
        document.addEventListener('submit', handleVoiceCommand);
        document.addEventListener('mouseover', handleVoiceCommand);
        document.addEventListener('select', handleVoiceCommand);
      } else {
        recognition.stop();
        recognition = null;

        document.getElementById('voiceCommandButton').textContent = 'Enable Voice Command';

        // Remove event listeners
        document.removeEventListener('click', handleVoiceCommand);
        document.removeEventListener('keydown', handleVoiceCommand);
        document.removeEventListener('change', handleVoiceCommand);
        document.removeEventListener('submit', handleVoiceCommand);
        document.removeEventListener('mouseover', handleVoiceCommand);
        document.removeEventListener('select', handleVoiceCommand);
      }
    }

    function handleSpeechResult(event) {
      const interimTranscript = event.results[event.results.length - 1][0].transcript;
      console.log('Interim Result:', interimTranscript);
    }

    function handleVoiceCommand(event) {
      const speechSynthesis = window.speechSynthesis;
      let utteranceText = 'Unknown content';

      if (event.type === 'click') {
        if (event.target.tagName === 'BUTTON') {
          utteranceText = 'Button clicked: ' + event.target.innerText;
        }
      } else if (event.type === 'change') {
        if (event.target.tagName === 'INPUT') {
          utteranceText = 'Input changed: ' + event.target.value;
        }
      } else if (event.type === 'mouseover') {
        utteranceText = 'Hovering over: ' + event.target.innerText;
      } else if (event.type === 'select') {
        utteranceText = 'Selected text: ' + window.getSelection().toString();
      } else if (event.type === 'keydown') {
        utteranceText = 'Key pressed: ' + event.key;
      }

      const utterance = new SpeechSynthesisUtterance(utteranceText);
      speechSynthesis.speak(utterance);
    }
  </script>
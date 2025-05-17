# DroneAI

A Python-based system for controlling drones using both hand gestures and voice commands, powered by AI and real-time computer vision. The project leverages Mediapipe for gesture recognition, Vosk for offline speech recognition, and Google Gemini (Generative AI) for interpreting natural language commands.

## Features

- **Gesture Control:** Use your hand gestures in front of a webcam to control drone directions and speed.
- **Voice Control:** Speak commands to control the drone, with natural language interpreted by Google Gemini.
- **Seamless Switching:** Switch between gesture and voice control modes using the keyword "switch".
- **Offline Speech Recognition:** Uses Vosk for robust, offline voice-to-text conversion.
- **Customizable AI:** Easily adapt the command interpretation rules in `src/ai.py`.

## Directory Structure

```
.
├── src/
│   ├── ai.py                # AI logic for interpreting commands
│   ├── command_recog.py     # Voice recognition and command handling
│   ├── gesture_classifier.py# Hand gesture recognition logic
│   └── main.py              # Main entry point for running the system
├── vosk-model-small-en-in-0.4/ # Vosk speech recognition model (Indian English)
├── .env                     # API key for Google Gemini
├── .gitignore
└── text_test.ipynb          # Notebook for testing AI command interpretation
```

## Requirements

- Python 3.8+
- Webcam (for gesture recognition)
- Microphone (for voice commands)

### Python Dependencies

Install the following packages (preferably in a virtual environment):

```bash
pip install opencv-python mediapipe numpy pyaudio vosk python-dotenv google-generativeai
```

> **Note:** You may need to install additional system dependencies for `pyaudio` (see [PyAudio installation docs](https://people.csail.mit.edu/hubert/pyaudio/)).

### Model Files

- Download the Vosk model (`vosk-model-small-en-in-0.4`) and place it in the project root (already present in this repo).

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd DroneAI
   ```

2. **Set up the environment:**
   - Create a `.env` file in the root directory with your Google Gemini API key:
     ```
     API_KEY = 'your-google-gemini-api-key'
     ```
   - (A sample `.env` is provided, but you should use your own API key.)

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is not present, use the list above.)*

4. **Run the application:**
   ```bash
   python src/main.py
   ```

## Usage

- **Gesture Mode:** Show your hand to the webcam and use gestures (see `gesture_classifier.py` for mapping).
- **Voice Mode:** Say commands like "go left", "move quickly", "brake", etc.
- **Switching Modes:** Say "switch" to toggle between gesture and voice control.

## Customization

- **Command Rules:** Edit `src/ai.py` to change how natural language is interpreted.
- **Gesture Logic:** Modify `src/gesture_classifier.py` for custom gesture mappings.

## Acknowledgements

- [Mediapipe](https://google.github.io/mediapipe/) for hand tracking.
- [Vosk](https://alphacephei.com/vosk/) for offline speech recognition.
- [Google Generative AI](https://ai.google.dev/) for natural language understanding. 
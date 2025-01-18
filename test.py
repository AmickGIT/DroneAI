import pyaudio
import json
from vosk import Model, KaldiRecognizer

class CommandRecognition:
    def __init__(self, receiver):
        self.model = Model("./vosk-model-small-en-in-0.4")
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.receiver = receiver  # Receiver class instance to send text to

    def start_listening(self):
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()

        print("Listening...")
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                result_dict = json.loads(result)  # Convert the JSON string into a Python dictionary
                text = result_dict.get('text', None)
                if text:
                    print("Recognized Text:", text)
                    self.receiver.receive_text(text)  # Send recognized text to the receiver

class Receiver:
    def __init__(self):
        pass

    def receive_text(self, text):
        print(f"Receiver got the text addes with ing: {text+"ing"}")
        # Here you can add logic to process the received text as needed

# Initialize and start the recognition process
receiver = Receiver()
recognition = CommandRecognition(receiver)
recognition.start_listening()

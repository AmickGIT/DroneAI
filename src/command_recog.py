from threading import Event
import pyaudio
import json
from ai import AI
from vosk import Model, KaldiRecognizer

class CommandRecognition:
    is_voice_controlled = False
    interpreted_text = "front and constant speed"
    def __init__(self, terminate_event: Event):
        self.model = Model("./vosk-model-small-en-in-0.4")
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.ai = AI()
        self.terminate_event = terminate_event

    def start_listening(self):
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()

        print("Listening...")
        while not self.terminate_event.is_set():
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                result_dict = json.loads(result) 
                text = result_dict.get('text', None)
                if text:
                    if self.is_voice_controlled:
                        print("Recognised text: ", text)
                        self.interpreted_text = self.ai.process_text(text) 
                        print("Interpreted text: ",self.interpreted_text)
                    try:
                        is_switch = int(self.ai.check_for_switch(text))
                        print(is_switch)
                        if is_switch == 1:
                            self.is_voice_controlled = not self.is_voice_controlled
                    except:
                        print("Try again")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Stopped listening.")

    def get_mode(self):
        return self.is_voice_controlled
    def get_command(self):
        return self.interpreted_text.strip()
        

# recognition = CommandRecognition()
# recognition.start_listening()
    

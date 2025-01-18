from vosk import Model, KaldiRecognizer
import pyaudio

class CommandRecognition():
    def __init__(self):
        model = Model("./vosk-model-small-en-in-0.4")
        recognizer = KaldiRecognizer(model, 16000)
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        print("Listening...")
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                print(result)
                if '"switch"' in result:
                    print("Stopping on user command...")
                    break
    

    

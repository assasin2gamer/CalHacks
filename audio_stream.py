import pyaudio
import wave
import time
import asyncio
import threading
import websockets
import pyaudio
from hume import HumeStreamClient
from hume.models.config import BurstConfig
from hume.models.config import ProsodyConfig
from pydub import AudioSegment
import os
import json

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILENAME = "output.wav"



async def main():
    while True:
        audio = pyaudio.PyAudio()

        # Create an audio stream
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("Recording...")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Finished recording.")

        # Stop and close the audio stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio as a WAV file
        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        uri = "ws://localhost:8765"

        # Initialize the HumeStreamClient
        client = HumeStreamClient("5i269G1jOVB286tGwN60X8bnnVokPQ56LnIQgfxBzBZRln5U")
        configs = [BurstConfig(), ProsodyConfig()]

        async with client.connect(configs) as socket:
            result = await socket.send_file("./output.wav")
            uri = "ws://localhost:8765" 
            sample_str = json.dumps(result)
            async with websockets.connect(uri) as websocket:
                await websocket.send(sample_str)

       
asyncio.get_event_loop().run_until_complete(main())

import asyncio
import websockets
import pyaudio

CHUNK = 50000  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Define a function to handle WebSocket connections
async def audio_stream(websocket, path):
    # Print a message when a client connects
    print(f"Client connected from {websocket.remote_address}")

    audio = pyaudio.PyAudio()

    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
        while True:
            data = await websocket.recv()
            stream.write(data)
            print("audio recieved")
    except websockets.exceptions.ConnectionClosedError:
        pass  # Connection closed by the client
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'stream' in locals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        if 'audio' in locals():
            audio.terminate()

# Set up the WebSocket server
start_server = websockets.serve(audio_stream, "localhost", 8765)

# Start the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


async with websockets.connect("ws://localhost:8765") as websocket:
    await websocket.send("SINGLE:YourSingleDataHere")

async with websockets.connect("ws://localhost:8765") as websocket:
    while True:
        await websocket.send("CONTINUOUS:YourContinuousDataHere")
        # Add a delay if needed
        await asyncio.sleep(1)  # Adjust the delay as needed
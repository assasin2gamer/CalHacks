import asyncio
import csv
import websockets
import json
from pylsl import StreamInlet, resolve_stream

async def send_eeg_data(uri):
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    async with websockets.connect(uri) as websocket:
        while True:
            # Get a new sample (you can omit the timestamp if not needed)
            sample, timestamp = inlet.pull_sample()

            # Convert the sample to a list of strings (assuming sample is a list)
            sample_str = json.dumps(sample)

            await websocket.send(sample_str)

if __name__ == '__main__':
    uri = "ws://localhost:8765"  # Replace with your WebSocket server address
    asyncio.get_event_loop().run_until_complete(send_eeg_data(uri))

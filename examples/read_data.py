import asyncio
import csv
import websockets

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
            sample_str = [str(value) for value in sample]

            # Send the EEG data as a JSON string over WebSocket
            await websocket.send(",".join(sample_str))  # Adjust the data format as needed

if __name__ == '__main__':
    uri = "ws://your_websocket_server_address"  # Replace with your WebSocket server address
    asyncio.get_event_loop().run_until_complete(send_eeg_data(uri))

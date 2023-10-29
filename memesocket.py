import asyncio
import websockets

# Dictionary to store client WebSocket connections
clients = set()

sendload = []


# Define a function to handle WebSocket connections
async def handle_connection(websocket, path):
    global sendload 
    # Add the client to the set of connected clients
    clients.add(websocket)
    print(f"Client connected from {websocket.remote_address}")

    try:
        async for message in websocket:
            # Check if the received message is a single data point
            if message.startswith("SINGLE:"):
                # Process single data point
                single_data = message[len("SINGLE:"):]
                print(f"Received single data: {single_data}")


                sendload = []


                # Handle the single data as needed

            # Check if the received message is continuous data
            elif message.startswith("["):
                # Process continuous data
                continuous_data = message[len("CONTINUOUS:"):]
                print(f"Received continuous data: {continuous_data}")
                sendload.append(continuous_data)
                # Handle the continuous data as needed

            else:
                print(f"Received unrecognized message: {message}")

    except websockets.exceptions.ConnectionClosedError:
        pass  # Connection closed by the client
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Remove the client from the set when they disconnect
        clients.remove(websocket)

def send(sendload, label):
    print(str(sendload), str(label))
# Set up the WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 8765)
# Start the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
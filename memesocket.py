import asyncio
import websockets
import psycopg2
import os
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
            if message.startswith("{"):
                # Process single data point
                single_data = message[len("SINGLE:"):]
                sendload = []
                send(sendload, single_data)


                # Handle the single data as neede

            # Check if the received message is continuous data
            elif message.startswith("["):
                # Process continuous data
                continuous_data = message[len("CONTINUOUS:"):]
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
   print('send')
   database_url ="postgresql://stephen:JqNZ8U622VuZfvZv25uXfw@howler-fawn-12542.7tt.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"
conn = psycopg2.connect(os.environ[database_url])
    with conn.cursor() as cur:
        cur.execute()
    conn.commit()

# Set up the WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 8765)
# Start the server
asyncio.get_event_loop().ruan_until_complete(start_server)
asyncio.get_event_loop().run_forever()
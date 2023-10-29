import asyncio
import websockets
import psycopg2
import os
import json
# Dictionary to store client WebSocket connections
clients = set()

sendload = []

insert_data_sql = """
INSERT INTO eeg_data (target, data)
VALUES (%s, %s)
"""

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
                send(sendload, single_data)

                sendload = []


                # Handle the single data as neede

            # Check if the received message is continuous data
            elif message.startswith("["):
                # Process continuous data
                if len(sendload) > 100:
                    sendload = sendload[50:]
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
    print(len(sendload), label)
    sendload = json.dumps(sendload)
    conn = psycopg2.connect('postgresql://t:yOQkfZS9LoTsvPL4fozvaA@good-stag-12544.7tt.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full')
    with conn.cursor() as cur:
        cur.execute(insert_data_sql, (label, sendload))
        conn.commit()
    
# Set up the WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 8765)
# Start the servers
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
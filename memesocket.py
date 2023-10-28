from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Define a global variable to store data
data_store = []

# Function to process data when it is received
def process_data(data):
    # You can define your data processing logic here
    print(f"Received data: {data}")

# Route for receiving continuous data
@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.json
    if data:
        data_store.append(data)
        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"message": "Invalid data"}), 400

# Function to continuously send data
def send_continuous_data():
    while True:
        # Simulate data generation (you can replace this with your data source)
        data_point = {"value": time.time()}
        # Send data to the server
        response = requests.post('http://localhost:5000/send_data', json=data_point)
        if response.status_code == 200:
            print("Continuous data sent successfully")
        time.sleep(1)  # Adjust the interval as needed

# Create a thread for sending continuous data
continuous_data_thread = threading.Thread(target=send_continuous_data)
continuous_data_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
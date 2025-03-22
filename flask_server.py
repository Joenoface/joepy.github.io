from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import pickle
import random

app = Flask(__name__)
CORS(app)

HOST = '127.0.0.1'
PORT = 65432

@app.route('/send_task', methods=['POST'])
def send_task():
    data = request.json
    task_data = data.get("task")

    if not task_data:
        return jsonify({"error": "No task provided"}), 400

    task_id = random.randint(1000, 9999)  # Unique task ID
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(pickle.dumps((task_id, task_data)))
        result = pickle.loads(s.recv(4096))

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

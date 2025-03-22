import socket
import pickle
import random

# Define server details
HOST = '127.0.0.1'
PORT = 65432

def send_task(task_data):
    task_id = random.randint(1000, 9999)  # Unique task ID
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(pickle.dumps((task_id, task_data)))
        result = pickle.loads(s.recv(4096))
    return result

if __name__ == "__main__":
    # Example task (can be changed)
    task = "sum(range(1000000))"  # Compute sum of first 1 million numbers
    result = send_task(task)
    print(f"Task Result: {result}")

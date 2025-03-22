import socket
import threading
import multiprocessing
import queue
import pickle

# Define server details
HOST = '127.0.0.1'
PORT = 65432

# Task queue for workers
task_queue = multiprocessing.Queue()
result_queue = multiprocessing.Queue()

# Worker function
def worker_function(task_queue, result_queue):
    while True:
        try:
            task_id, task_data = task_queue.get()  # Get task from queue
            if task_data is None:
                break  # Stop worker if termination signal received
            result = eval(task_data)  # Execute task (safe environment should be enforced)
            result_queue.put((task_id, result))
        except Exception as e:
            result_queue.put((task_id, f"Error: {e}"))

# Server handling client requests
def handle_client(client_socket):
    try:
        data = client_socket.recv(4096)
        if not data:
            return
        
        # Deserialize the received task
        task_id, task_data = pickle.loads(data)
        
        # Push the task into the queue
        task_queue.put((task_id, task_data))

        # Wait for the result
        while True:
            try:
                result_task_id, result = result_queue.get(timeout=5)
                if result_task_id == task_id:
                    client_socket.send(pickle.dumps(result))
                    break
            except queue.Empty:
                continue

    finally:
        client_socket.close()

# Start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    # Start worker processes
    num_workers = multiprocessing.cpu_count()
    workers = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker_function, args=(task_queue, result_queue))
        p.start()
        workers.append(p)

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()

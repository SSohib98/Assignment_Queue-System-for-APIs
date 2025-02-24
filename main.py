import numpy as np
import queue
import threading
import multiprocessing
import time
import random

class MatrixMultiplicationQueue:
    def __init__(self, queue_size=10, num_workers=4):
        # Set queue size and worker configurations
        self.queue = queue.Queue(maxsize=queue_size)
        self.num_workers = num_workers
        self.is_running = True

    def matrix_multiply(self, matrix1, matrix2):
        """Simulate matrix multiplication using numpy's matmul function."""
        return np.matmul(matrix1, matrix2)

    def worker_thread(self):
        """Worker thread to process requests from the queue."""
        while self.is_running:
            try:
                matrix1, matrix2 = self.queue.get(timeout=1)  # Get an item from the queue
                result = self.matrix_multiply(matrix1, matrix2)
                print(f"Processed result with shape {result.shape}")
            except queue.Empty:
                continue

    def worker_process(self):
        """Worker process to process requests from the queue."""
        while self.is_running:
            try:
                matrix1, matrix2 = self.queue.get(timeout=1)  # Get an item from the queue
                result = self.matrix_multiply(matrix1, matrix2)
                print(f"Processed result with shape {result.shape}")
            except queue.Empty:
                continue

    def start_threads(self):
        """Start multiple worker threads."""
        threads = []
        for _ in range(self.num_workers):
            thread = threading.Thread(target=self.worker_thread)
            thread.daemon = True
            threads.append(thread)
            thread.start()
        return threads

    def start_processes(self):
        """Start multiple worker processes."""
        processes = []
        for _ in range(self.num_workers):
            process = multiprocessing.Process(target=self.worker_process)
            process.daemon = True
            processes.append(process)
            process.start()
        return processes

    def add_to_queue(self, matrix1, matrix2):
        """Add a matrix multiplication task to the queue."""
        if not self.queue.full():
            self.queue.put((matrix1, matrix2))
        else:
            print("Queue is full, task dropped.")

    def stop(self):
        """Stop the queue processing."""
        self.is_running = False

    def test_flooding(self, call_rate=1):
        """Simulate flooding by adding requests at a given rate."""
        for _ in range(call_rate):
            matrix1 = np.random.rand(1000, 1000)  # Large matrix 1000x1000
            matrix2 = np.random.rand(1000, 1000)
            self.add_to_queue(matrix1, matrix2)

    def stress_test(self, call_rate=100):
        """Test with multiple calls per second."""
        self.test_flooding(call_rate)


if __name__ == "__main__":
    # Test configuration
    queue_size = 20
    num_workers = 4  # Number of worker threads or processes
    call_rate = 10  # Requests per second
    mode = "thread"  # Choose between "thread" or "process"

    queue_system = MatrixMultiplicationQueue(queue_size=queue_size, num_workers=num_workers)

    # Start threads or processes based on user mode
    if mode == "thread":
        queue_system.start_threads()
    elif mode == "process":
        queue_system.start_processes()

    # Simulate requests flooding at the specified rate
    queue_system.stress_test(call_rate=call_rate)

    # Let the system process for a while (simulate work time)
    time.sleep(10)

    # Stop the queue system
    queue_system.stop()
    print("Queue processing stopped.")

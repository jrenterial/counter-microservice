import zmq
import json

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558")
    print("Client connected to Counter Microservice...")

    # Test 1: Increment a new counter
    print("Test 1: Increment new counter:")
    payload = {"action": "counter", "counter_name": "test_counter"}
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    print(response)  # Should show count: 1

    # Test 2: Increment again (should be 2)
    print("\nTest 2: Increment again:")
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    print(response)  # Should show count: 2

    # Test 3: Reset the counter
    print("\nTest 3: Reset counter:")
    reset_payload = {"action": "reset", "counter_name": "test_counter"}
    socket.send_string(json.dumps(reset_payload))
    response = json.loads(socket.recv_string())
    print(response)  # Should show count: 0

    # Test 4: Increment after reset
    print("\nTest 4: Increment after reset:")
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    print(response)  # Should show count: 1

    # Test 5: Get Count
    print("\nTest 5: Get Count:")
    get_payload = {"action": "get", "counter_name": "test_counter"}
    socket.send_string(json.dumps(get_payload))
    response = json.loads(socket.recv_string())
    print(response)  # Should show count: 1

    # Test 6: Error Handling - Invalid Action
    print("\nTest 6: Invalid Action:")
    payload = {"action": "delete", "counter_name": "test_counter"}
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    print(response)  # Status: error

    # Test 7: Missing Counter Name
    print("\nTest 7: Get non-existing counter:")
    get_payload = {"action": "get", "counter_name": "test_counter1"}
    socket.send_string(json.dumps(get_payload))
    response = json.loads(socket.recv_string())
    print(response)  # Status: error

    # Test 8: Counter Name missing
    print("\nTest 8: Increment new counter:")
    payload = {"action": "counter", "counter_name": ""}
    socket.send_string(json.dumps(payload))
    response = json.loads(socket.recv_string())
    print(response)  # Status error

    # Test 9: Multiple counters are independent
    print("\nTest 9: Multiple counters:")
    payload1 = {"action": "counter", "counter_name": "user_logins"}
    socket.send_string(json.dumps(payload1))
    response = json.loads(socket.recv_string())
    print(f"user_logins: {response}")  # Should be 1

    payload2 = {"action": "counter", "counter_name": "emails_sent"}
    socket.send_string(json.dumps(payload2))
    response = json.loads(socket.recv_string())
    print(f"emails_sent: {response}")  # Should be 1

    # Increment user_logins again
    socket.send_string(json.dumps(payload1))
    response = json.loads(socket.recv_string())
    print(f"user_logins again: {response}")  # Should be 2

    # Test 10: Reset non-existent counter
    print("\nTest 10: Reset non-existent counter:")
    reset_payload = {"action": "reset", "counter_name": "doesnt_exist"}
    socket.send_string(json.dumps(reset_payload))
    response = json.loads(socket.recv_string())
    print(response)  # Status error

if __name__ == "__main__":
    main()
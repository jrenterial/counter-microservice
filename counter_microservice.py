import zmq
import json

# Hold counters
counters = {}

def success_response(counter_name, count):
    """
    Desc: Generate a success response
    Input: counter_name (str), count (int)
    Output: None
    Return: dict with status ok, counter_name, and count
    """
    return {
        "status": "ok",
        "counter_name": counter_name,
        "count": count
    }

def error_response(counter_name, message):
    """
    Desc: Generate an error response
    Input: counter_name (str), message (str)
    Output: None
    Return: dict with status error, counter_name, and error message
    """
    return {
        "status": "error",
        "counter_name": counter_name,
        "message": message
    }

def counter(data):
    """
    Desc: Increment a counter by 1, creating it if it doesn't exist
    Input: data (dict) - must contain "counter_name" key
    Output: None
    Return: Success response with updated count or error response
    """

    counter_name = data.get("counter_name", "")

    # Check name is not empty
    if not counter_name:
        return error_response(counter_name, "counter_name is required")

    # initialize counter
    if counter_name not in counters:
        counters[counter_name] = 0

    # Increment counter
    counters[counter_name] += 1

    #return counter
    return success_response(counter_name, counters[counter_name])

def reset_count(data):
    """
    Desc: Reset a counter to 0
    Input: data (dict) - must contain "counter_name" key
    Output: None
    Return: Success response with count 0 or error if counter doesn't exist
    """
    
    counter_name = data.get("counter_name", "")
    
    if counter_name not in counters:
        return error_response(counter_name, "Counter does not exist")
    
    # Reset counter
    counters[counter_name] = 0
    return success_response(counter_name, counters[counter_name])

def get_count(data):
    """
    Desc: Get the current count of a counter without modifying it
    Input: data (dict) - must contain "counter_name" key
    Output: None
    Return: Success response with current count or error if counter doesn't exist
    """

    counter_name = data.get("counter_name", "")

    if counter_name in counters:
        return success_response(counter_name, counters[counter_name])
    
    return error_response(counter_name, "Counter does not exist")


ACTION_MAP = {
    
    "counter": counter,
    "reset": reset_count,
    "get": get_count
}

def process_request(data):
    """
    Desc: Route incoming requests to the appropriate handler function
    Input: data (dict) - must contain "action" key
    Output: None
    Return: Response dictionary from the handler function
    """
    
    action = data.get("action", "").strip()
    
    if action not in ACTION_MAP:
        return{
            "status": "error",
            "message": f"Invalid action: {action}"
        }

    handler = ACTION_MAP.get(action)
    return handler(data) 


def main():
    """
    Desc: Start the ZeroMQ server and listen for authentication requests.
    Input: None
    Output: Prints server status, processes incoming requests
    Return: None
    """

    # Setup ZeroMQ
    context = zmq.Context()

    # REP socket
    socket = context.socket(zmq.REP)

    socket.bind("tcp://*:5558")
    print("Counter Microservice listening on tcp://*:5558")
    
    while True:

        message = socket.recv_string()
        print("Server Received: ", message)

        try:
            data = json.loads(message)
        except json.JSONDecodeError:

            # Check if valid JSON
            socket.send_string(json.dumps(("Invalid JSON")))
            continue

        # Get action
        reply_data = process_request(data)

        # Convert to JSON string
        reply_json = json.dumps(reply_data)

        # Send reply back to the client
        socket.send_string(reply_json)

if __name__ == "__main__":
    main()
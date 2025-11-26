# Counter Microservice

A generic counter utility microservice that allows clients to track, increment, reset, and retrieve counts for any named counter.

## Description

This microservice provides a flexible counting system that can be used to track various metrics across different applications. Each counter is identified by a unique name, allowing multiple independent counters to run simultaneously.

**Common use cases:**
- Track failed login attempts
- Count emails sent
- Monitor contacts added
- Track daily activities
- Any other counting needs

## Prerequisites

- Python 3.x
- PyZMQ library (`pip install pyzmq`)

## How to Run

1. Start the Counter microservice:
```bash
python counter_service.py
```

The service will start listening on `tcp://*:5558`

## API Documentation

### Request Format

All requests must be sent as JSON strings with the following structure:
```json
{
    "action": "counter|reset|get",
    "counter_name": "your_counter_name"
}
```

### Available Actions

#### 1. Increment Counter (`counter`)
Increments the specified counter by 1. Creates the counter if it doesn't exist.

**Request:**
```json
{
    "action": "counter",
    "counter_name": "user_123_failed_logins"
}
```

**Success Response:**
```json
{
    "status": "ok",
    "counter_name": "user_123_failed_logins",
    "count": 3
}
```

#### 2. Get Counter (`get`)
Retrieves the current count without modifying it.

**Request:**
```json
{
    "action": "get",
    "counter_name": "user_123_failed_logins"
}
```

**Success Response:**
```json
{
    "status": "ok",
    "counter_name": "user_123_failed_logins",
    "count": 3
}
```

**Error Response (counter doesn't exist):**
```json
{
    "status": "error",
    "counter_name": "user_123_failed_logins",
    "message": "Counter does not exist"
}
```

#### 3. Reset Counter (`reset`)
Resets the specified counter to 0.

**Request:**
```json
{
    "action": "reset",
    "counter_name": "user_123_failed_logins"
}
```

**Success Response:**
```json
{
    "status": "ok",
    "counter_name": "user_123_failed_logins",
    "count": 0
}
```

**Error Response (counter doesn't exist):**
```json
{
    "status": "error",
    "counter_name": "user_123_failed_logins",
    "message": "Counter does not exist"
}
```

### Error Responses

#### Invalid Action
```json
{
    "status": "error",
    "message": "Invalid action: delete"
}
```

#### Missing Counter Name
```json
{
    "status": "error",
    "counter_name": "",
    "message": "counter_name is required"
}
```

## Example Usage

### Python Client Example
```python
import zmq
import json

# Setup connection
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5558")

# Increment a counter
payload = {"action": "counter", "counter_name": "emails_sent"}
socket.send_string(json.dumps(payload))
response = json.loads(socket.recv_string())
print(response)  # {"status": "ok", "counter_name": "emails_sent", "count": 1}

# Get current count
payload = {"action": "get", "counter_name": "emails_sent"}
socket.send_string(json.dumps(payload))
response = json.loads(socket.recv_string())
print(response)  # {"status": "ok", "counter_name": "emails_sent", "count": 1}

# Reset counter
payload = {"action": "reset", "counter_name": "emails_sent"}
socket.send_string(json.dumps(payload))
response = json.loads(socket.recv_string())
print(response)  # {"status": "ok", "counter_name": "emails_sent", "count": 0}
```

## Testing

Run the test suite to verify functionality:
```bash
# In one terminal, start the service
python counter_service.py

# In another terminal, run tests
python counter_test.py
```

The test file will run through various scenarios including:
- Incrementing new counters
- Multiple increments
- Resetting counters
- Getting counts
- Error handling
- Multiple independent counters

## Configuration

- **Port:** 5558
- **Protocol:** TCP
- **Message Format:** JSON

## Notes

- Each counter is independent and tracked by its unique `counter_name`
- Counters are stored in memory and will reset when the service restarts
- Counter names are case-sensitive
- Multiple clients can use the same counter simultaneously

## Author

Jose R. - CS361 - OSU: Fall 2025
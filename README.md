# CMPE 148 Web Server Lab

This repository contains the implementation of a basic HTTP web server in Python as part of the CMPE 148 lab assignment.

## Lab Overview

In this lab, we learn the basics of socket programming for TCP connections in Python, including:
- Creating and binding sockets
- Sending and receiving HTTP packets
- Understanding HTTP header format
- Handling HTTP requests and responses

## Files in This Repository

### Core Implementation
- `webserver.py` - Complete implementation of the basic single-threaded web server
- `HelloWorld.html` - Test HTML file for the server
- `multithreaded_webserver.py` - Optional multithreaded version that handles multiple concurrent requests
- `client.py` - Custom HTTP client for testing the server

### Test Files
- `HelloWorld.html` - Sample HTML file for testing

## How to Run

### Running the Basic Web Server

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the server:
   ```bash
   python webserver.py
   ```
4. The server will start listening on port 6789
5. Open a web browser and navigate to: `http://localhost:6789/HelloWorld.html`

### Running the Multithreaded Web Server

1. Run the multithreaded version:
   ```bash
   python multithreaded_webserver.py
   ```
2. This version can handle multiple requests simultaneously

### Using the Custom HTTP Client

Instead of a browser, you can test the server using the custom client:

```bash
python client.py localhost 6789 HelloWorld.html
```

**Command format:**
```bash
python client.py server_host server_port filename
```

## Features Implemented

### Basic Web Server (`webserver.py`)
- ✅ Accepts HTTP GET requests
- ✅ Serves HTML files from the same directory
- ✅ Returns proper HTTP 200 OK responses for existing files
- ✅ Returns HTTP 404 Not Found for missing files
- ✅ Handles one request at a time

### Multithreaded Web Server (`multithreaded_webserver.py`)
- ✅ All basic server features
- ✅ Handles multiple concurrent requests using threading
- ✅ Each client connection runs in a separate thread
- ✅ Improved error handling and logging
- ✅ Graceful shutdown with Ctrl+C

### HTTP Client (`client.py`)
- ✅ Connects to server using TCP socket
- ✅ Sends HTTP GET requests
- ✅ Displays server responses
- ✅ Command-line interface
- ✅ Error handling for connection issues

## Testing the Server

### Test 1: Valid File Request
1. Start the server: `python webserver.py`
2. In browser, go to: `http://localhost:6789/HelloWorld.html`
3. **Expected Result**: The HTML page should display properly

### Test 2: Missing File (404 Error)
1. With server running, go to: `http://localhost:6789/nonexistent.html`
2. **Expected Result**: "404 Not Found" error message

### Test 3: Using Custom Client
1. Start server: `python webserver.py`
2. In another terminal: `python client.py localhost 6789 HelloWorld.html`
3. **Expected Result**: HTTP response printed to console

### Test 4: Concurrent Requests (Multithreaded Server)
1. Start multithreaded server: `python multithreaded_webserver.py`
2. Open multiple browser tabs to `http://localhost:6789/HelloWorld.html`
3. **Expected Result**: All requests should be handled simultaneously

## Key Learning Points

1. **Socket Programming**: Understanding TCP socket creation, binding, and communication
2. **HTTP Protocol**: Learning HTTP request/response format and status codes
3. **File I/O**: Reading files from the server filesystem
4. **Error Handling**: Proper handling of missing files and connection errors
5. **Threading**: Implementing concurrent request handling
6. **Client-Server Communication**: Building both server and client applications

## Technical Details

### Server Configuration
- **Port**: 6789
- **Host**: localhost (127.0.0.1)
- **Protocol**: HTTP/1.1
- **Supported Methods**: GET

### HTTP Response Format
```
HTTP/1.1 200 OK\r\n\r\n
[File Content]
```

### Error Response Format (404)
```
HTTP/1.1 404 Not Found\r\n\r\n
<html><head></head><body><h1>404 Not Found</h1></body></html>
```

## Code Structure

### Main Server Loop
1. Create and bind socket
2. Listen for connections
3. Accept client connections
4. Parse HTTP request
5. Extract requested filename
6. Try to read and serve file
7. Send appropriate HTTP response
8. Close connection

### Error Handling
- **IOError**: File not found → 404 response
- **Socket errors**: Connection issues
- **Malformed requests**: Basic error handling

## Optional Enhancements Implemented

1. **Multithreading**: Server can handle multiple concurrent requests
2. **Custom HTTP Client**: Alternative to browser testing
3. **Enhanced Error Handling**: Better error messages and logging
4. **Graceful Shutdown**: Proper cleanup on server termination

## Requirements Met

- ✅ Complete skeleton code implementation
- ✅ HTTP request parsing
- ✅ File serving functionality
- ✅ 404 error handling
- ✅ Multithreaded server (optional)
- ✅ Custom HTTP client (optional)
- ✅ Comprehensive documentation
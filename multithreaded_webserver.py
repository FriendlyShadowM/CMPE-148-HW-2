#import socket module and threading
from socket import * 
import sys # In order to terminate the program
import threading

def handle_client(connectionSocket, addr):
    """Handle a single client connection in a separate thread"""
    try: 
        message = connectionSocket.recv(1024).decode()
        print(f'Handling request from {addr}: {message.split()[0]} {message.split()[1]}')
        
        filename = message.split()[1]                  
        f = open(filename[1:])                         
        outputdata = f.read()
        f.close()
        
        #Send one HTTP header line into socket 
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
        connectionSocket.send(header.encode())
        
        #Send the content of the requested file to the client 
        connectionSocket.send(outputdata.encode()) 
        
    except IOError: 
        #Send response message for file not found 
        print(f'File not found for request from {addr}')
        header = 'HTTP/1.1 404 Not Found\r\n\r\n'
        connectionSocket.send(header.encode())
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'.encode())
    
    except Exception as e:
        print(f'Error handling client {addr}: {e}')
        header = 'HTTP/1.1 500 Internal Server Error\r\n\r\n'
        connectionSocket.send(header.encode())
        connectionSocket.send('<html><head></head><body><h1>500 Internal Server Error</h1></body></html>\r\n'.encode())
    
    finally:
        #Close client socket 
        connectionSocket.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM) 
    
    #Prepare a server socket 
    serverSocket.bind(('', 6789))
    serverSocket.listen(5)  # Allow up to 5 connections in queue
    print('Multithreaded server started on port 6789')
    print('Server can handle multiple concurrent connections')
    
    try:
        while True: 
            #Establish the connection 
            print('Ready to serve...') 
            connectionSocket, addr = serverSocket.accept()
            print(f'Connection established with {addr}')
            
            # Create a new thread to handle this client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(connectionSocket, addr),
                daemon=True  # Thread will die when main program exits
            )
            client_thread.start()
            
    except KeyboardInterrupt:
        print('\nServer shutting down...')
    finally:
        serverSocket.close() 
        sys.exit()

if __name__ == "__main__":
    main()
#import socket module 
from socket import * 
import sys # In order to terminate the program 

def run_server():
    """Run the web server"""
    serverSocket = socket(AF_INET, SOCK_STREAM) 

    #Prepare a sever socket 
    #Fill in start 
    serverSocket.bind(('', 6789))
    serverSocket.listen(1)
    #Fill in end 

    try:
        while True: 
            #Establish the connection 
            print('Ready to serve...') 
            connectionSocket, addr = serverSocket.accept()
            
            try: 
                message = connectionSocket.recv(1024).decode()
                #Fill in start              #Fill in end           
                
                #Fill in start          #Fill in end                
                filename = message.split()[1]                  
                f = open(filename[1:])                         
                outputdata = f.read()
                f.close()
                #Fill in start       #Fill in end                    
                
                #Send one HTTP header line into socket 
                #Fill in start 
                header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(len(outputdata)) + '\r\n\r\n'
                connectionSocket.send(header.encode())
                #Fill in end                 
                
                #Send the content of the requested file to the client 
                for i in range(0, len(outputdata)):            
                    connectionSocket.send(outputdata[i].encode())
                # connectionSocket.send(outputdata.encode())
                connectionSocket.close() 
                
            except IOError: 
                #Send response message for file not found 
                #Fill in start         
                header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                connectionSocket.send(header.encode())
                connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'.encode())
                #Fill in end 
                
                #Close client socket 
                #Fill in start 
                connectionSocket.close()
                #Fill in end             
    except KeyboardInterrupt:
        print('\nServer shutting down...')
    finally:
        serverSocket.close() 
        sys.exit()#Terminate the program after sending the corresponding data                                    

if __name__ == "__main__":
    run_server()                                    
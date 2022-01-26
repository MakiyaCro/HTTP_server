# import socket module
from socket import *
from datetime import datetime

# Create serverSocket
serverPort = 7777
serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a seversocket with port #
serverSocket.bind(('', serverPort))
serverSocket.listen(3)
print("The web server is up on port: ", str(serverPort))
rnow = datetime.now()
init = rnow.strftime("%A, %d %m %Y %H:%M:%S GMT")
while True:

    print('Ready to serve...')
    # generate connection socket and establish the connection
    connectionSocket, addr = serverSocket.accept()
    rnow = datetime.now()
    dt_string = rnow.strftime("%A, %d %m %Y %H:%M:%S GMT")

    newdate = 0
    try:
        # receive HTTP request
        message = connectionSocket.recv(4096).decode()
        try:

            # tokenize HTTP message header

            nday = message.split()[41]
            print(nday)
            day = message.split()[42]
            print(day)
            month = message.split()[43]
            print(month)
            year = message.split()[44]
            print(year)
            time = message.split()[45]
            print(time)
            newdate = nday + ' ' + day + ' ' + month + ' ' + year + ' ' + time + ' GMT'
        except:
            pass

        # find filename in the message string array (use split function)
        filename = message.split()[1]
        if newdate != 0:
            # check to see if the modified date has changed since the start of the server
            if newdate != init:  # if it has re output file info
                init = newdate
                f = open(filename[1:])
                outputdata = f.read()
                f.close()
                # print (str(outputdata))
                # Send one HTTP header line into socket
                # 200 send info
                connectionSocket.send(
                    bytes("\nHTTP/1.1 200 OK\r\nLast-Modified: " + init + "\r\nDate: " + dt_string + "\r\n\r\n",
                          "utf-8"))

                # Send the content of the requested file to the client
                connectionSocket.send(bytes(outputdata, "utf-8"))
            # 304 send info
            else:

                connectionSocket.send(bytes("\nHTTP/1.1 304 Not-Modified\r\nLast-Modified: " + init + "\r\nDate: " + dt_string + "\r\n\r\n", "utf-8"))
        else:
            # open file and read contents
            f = open(filename[1:])
            outputdata = f.read()
            f.close()
            # print (str(outputdata))
            # Send one HTTP header line into socket
            # 200 send info
            connectionSocket.send(
                bytes("\nHTTP/1.1 200 OK\r\nLast-Modified: " + init + "\r\nDate: " + dt_string + "\r\n\r\n", "utf-8"))

            # Send the content of the requested file to the client
            connectionSocket.send(bytes(outputdata, "utf-8"))
        # close connection socket
        connectionSocket.close()

        # except IOError:

    except IOError:
        # Send response message for file not found
        # Fill in start
        connectionSocket.send(bytes("\nHTTP/1.1 404 Not Found\n\n", "utf-8"))
        connectionSocket.send(bytes("<html><head><title>404 Not Found</title></head><body><h1>NotFound</h1><p>The requested URL was not found on this server.</p></body></html>","utf-8"))


        #other exceptions
    except Exception:
        connectionSocket.send(bytes("Other Error Detected", "utf-8"))


import socket
import threading
from pyautogui import press

############# Add Server Here ##################
SERVER = "example.com"
################################################


RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
RESET = "\u001b[0m"

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, 9999))
    print("Connected to server.")

    client_socket.send("R".encode())
    data = client_socket.recv(1024).decode()
    if data and len(data) >= 1:
        print("")
        print("                 %s┏━━━━━━┓%s" % (GREEN, RESET))
        print("Received secret: %s┃ %s%s%s ┃%s" % (GREEN, YELLOW, data[1:].upper(), GREEN, RESET))
        print("                 %s┗━━━━━━┛%s" % (GREEN, RESET))
        print("")
    
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data and len(data) >= 1:
                if data[0] == 'K':
                    if data[1:] == "<next>":
                        print("Next slide")
                        press("pagedown")
                    elif data[1:] == "<prev>":
                        print("Previous slide")
                        press("pageup")
                    else:
                        print("%sUnknown key!%s" % (RED, RESET))
                elif data[0] == 'B':
                    print("Received exit command, exiting")
                    client_socket.close()
                    sys.exit(0)
                else:
                    print("Received unknown data: %s" % data)


        except KeyboardInterrupt:
            client_socket.send("B".encode())
            client_socket.close()
            print("Connection closed.")
        except socket.error:
            print("Closing, connection died")
            break

if __name__ == '__main__':
    start_client()
 

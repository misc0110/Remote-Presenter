import socket
import threading
import random
import string
import time

timeout = 60 * 60 * 8 # 8 hours



receivers = {}
senders = {}
running = True

def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def cleanup():
    global receivers, senders
    dl = []
    for s in senders:
        if time.time() > senders[s]["last_active"] + timeout:
            dl.append(s)
    for s in dl:
        del senders[s]
    dl = []
    for r in receivers:
        if time.time() > receivers[r]["last_active"] + timeout:
            dl.append(r)
    for r in dl:
        del receivers[r]
    print("%d receivers, %d senders active" % (len(receivers), len(senders)))


def handle_client(client_socket):
    global receivers, senders
    while running:
        try:
            data = client_socket.recv(1024)
        except:
            if client_socket in senders:
                print("Client for %s gone" % senders[client_socket]["secret"])
                senders[client_socket]["last_active"] = 0
                cleanup()
            print("Goodbye!")
            break
        if len(data) == 0:
            break

        #print(data)
        if data and len(data) >= 1:
            d = data.decode()
            action = d[0]
            if action == 'R':
                secret = get_random_string(4)
                receivers[secret] = {"socket": client_socket, "last_active": time.time()}
                client_socket.send(("R%s" % secret).encode())
            elif action == 'S':
                secret = d[1:]
                if secret in receivers:
                    client_socket.send("sOK".encode())
                    senders[client_socket] = {"secret": secret, "last_active": time.time()}
                else:
                    client_socket.send("sNOTFOUND".encode())
            elif action == 'K':
                if client_socket in senders:
                    secret = senders[client_socket]["secret"]
                    try:
                        receivers[secret]["socket"].send(data)
                        client_socket.send("sOK".encode())
                    except:
                        print("Receiver is gone")
                        client_socket.send("sGONE".encode())
                        if secret in receivers:
                            receivers[secret]["last_active"] = 0
                        cleanup()
                else:
                    try:
                        client_socket.send("sNOTFOUND".encode())
                    except:
                        pass
            elif action == 'B':
                if client_socket in senders:
                    print("Sender for %s disconnected" % senders[client_socket]["secret"])
                    senders[client_socket]["last_active"] = 0
                    cleanup()
                else:
                    for r in receivers:
                        if receivers[r]["socket"] == client_socket:
                            print("Receiver %s disconnecting, notify sender" % r)
                            for s in senders:
                                if senders[s]["secret"] == r:
                                    print(" - found one, notify")
                                    try:
                                        s.send("sBYE".encode())
                                    except:
                                        pass
                                    senders[s]["last_active"] = 0
                            receivers[r]["last_active"] = 0
                    cleanup()


def start_server():
    global running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(1)
    print("Server started. Listening for connections...")

    try:
        while running:
            client1, address1 = server_socket.accept()
            print("Client connected from: ", address1)
            
            cleanup()
            
            thread = threading.Thread(target=handle_client, args=(client1, ))
            thread.start()

    except KeyboardInterrupt:
        running = False
        server_socket.close()
        print("Server stopped.")

if __name__ == '__main__':
    start_server()
 

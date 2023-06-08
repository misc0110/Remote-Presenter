import socket
import threading
hook_start = False
try:
    import pyxhook
    hook_start = True
except:
    import pyWinhook as pyxhook
    import pythoncom
import sys

############# Add Server Here ##################
SERVER = "example.com"
################################################


client_socket = None
new_hook = None
running = True

ctrl = False
def OnKeyPress(event):
    #client_socket.send("K<next>".encode())
    global ctrl, running
    
    if not hook_start:
        if event.Key == "Lcontrol":
            ctrl = True
            return True
        if event.Key == "C" and ctrl:
            running = False
            sys.exit(1)
        ctrl = False

    if event.Key == "Next" or event.Key == "Page_Down":
        client_socket.send("K<next>".encode())
    elif event.Key == "Prior" or event.Key == "Page_Up":
        client_socket.send("K<prev>".encode())
    return True

RED = "\u001b[31m"
GREEN = "\u001b[32m"
RESET = "\u001b[0m"

def handle_error(err):
    global running
    do_exit = True
    if err == "BYE" or err == "GONE":
        print("%sReceiver exited, exiting...%s" % (RED, RESET))
    if err == "NOTFOUND":
        print("%sReceiver not found, exiting%s" % (RED, RESET))
    if do_exit:
        running = False
        if new_hook and hook_start:
            new_hook.cancel()
            try:
                _thread.interrupt_main()
            except:
                pass
            sys.exit(1)
        

def handle_status():
    while running:
        try:
            data = client_socket.recv(1024)
            if data:
                d = data.decode()
                if d[0] == "s":
                    if d[1:] == "BYE" or d[1:] == "GONE" or d[1:] == "NOTFOUND":
                        handle_error(d[1:])
                    elif d[1:] == "OK":
                        print("Key received")
                else:
                    print(d)
        except:
            pass


def start_client():
    global client_socket, new_hook
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(1)
    client_socket.connect((SERVER, 9999))
    print("Connected to server.\n")
    
    secret = input("Enter server code: ").lower()
    print("")

    client_socket.send(("S%s" % secret).encode())
    data = client_socket.recv(1024).decode()
    if data and len(data) >= 1:
        if data[1:] == "NOTFOUND":
            handle_error(data[1:])
        if data[1:] == "OK":
            print("%sConnected to server!%s" % (GREEN, RESET))
        else:
            print("Received: %s" % data[1:])

    receive_thread = threading.Thread(target=handle_status)
    receive_thread.start()

    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress
    new_hook.HookKeyboard()
    try:
        if hook_start:
            new_hook.start()
        else:
            pythoncom.PumpMessages()
    except KeyboardInterrupt:
        client_socket.send("B".encode())
        client_socket.close()
        if hook_start:
            new_hook.cancel()
        print("Connection closed.")


if __name__ == '__main__':
    start_client()
 

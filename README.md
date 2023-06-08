# Remote Presenter
Wireless presenters are great if all presenters are at the same physical location. 
However, with remote presentations, this is not always the case, and a different solution is needed. 
This is precisely where this project comes to the rescue: it forwards the buttons of a wireless presenter over the internet to the target computer. 
Consequently, presenters can be all over the world and still advance slides on the presenting machine.

## Requirements

The remote presenter software is implemented in Python and works on Windows and Linux. 
It requires a publicly-reachable handshake server to allow connections behind firewalls, i.e., any home network. 

### Server
The server can be run as a docker container. 
It requires port 9999 to be open. 
To run the server:

```
docker-compose up -d
```

The URL of the server has to be added to both `sender.py` and `receiver.py`. 

### Linux
On Linux, the `pyautogui` is required on the receiver side to inject the buttons.
`pyxhook` and an X server is required on the sender side to hook the buttons of a wireless presenter.
Both can be installed via pip:

```
pip3 install pyautogui pyxhook
```

### Windows
On Windows, the `pyautogui` is required on the receiver side to inject the buttons.
`pywinhook` is required on the sender side to hook the buttons of a wireless presenter.
Both can be installed via pip:

```
python3 -m pip install --user pyautogui pywinhook
```

## Usage
On the receiver machine, i.e., the machine that has the presentation, the `receiver.py` tool has to be started. 
When starting, it displays a 4-letter code required on the sender side to connect to the correct receiver. 
Every machine that wants to act as a remote presenter runs the `sender.py` tool and enters the 4-letter code when asked.
If the code is correct, the machines are paired, and "next" and "previous" presses of a presenter are forwarded to the receiving machine. 


client.exe appeared to be timing out while attempting to make a server connection (as its name would imply). Step 1 is to monitor outgoing local traffic to determine what port client.exe was trying to connect to, to set up a server to listen.

In CMD:
netstat -ano -p tcp
```
  TCP    127.0.0.1:57839        127.0.0.1:57742        ESTABLISHED     29720
  TCP    127.0.0.1:58008        127.0.0.1:8123         SYN_SENT        10508
  TCP    127.0.0.1:59604        127.0.0.1:65001        ESTABLISHED     5320
```

By diffing local traffic before and while running client.exe we determine then 

In python:

import socket

```
if __name__ == '__main__':
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 8123  # Port to listen on (non-privileged ports are > 1023)

    message = list()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message.append(data)

    print(message)
```

This results in the following bitstream:

```
[b'6264 0000 new odtga = 52\r\nnew hi = 29\r\nnew iy = 13\r\nnew na = 72\r\n??((((((odtga))))-60+hi) <= (iy+na-58))\r\nR0lGODlh9AF3AfY5ABWj3QYDEA+NyAJllzit5iXK/AUkVyTZ/ydKe...
```

At this point, we make the following observations:
- The sequential 4-digit codes that are sprinkled throughout (e.g. 0000) are probably just chunk number and not part of the message
- The constructed programming language appears to be a series of variable declarations and control statements beginning with double question marks. Most of these appeared to evaluate to TRUE.
  - This might be criteria of whether or not to include or exclude certain chunks in the encrypted message body
- The message body appears to be composed of mostly alphanumeric characters but also has `/` and `+` sprinkled throughout. These might also be control characters.

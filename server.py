import socket

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

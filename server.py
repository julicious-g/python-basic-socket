import socket
import threading

HEADER = 64  # bit
PORT = 5050
SERVER = 'localhost'
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECTED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn: socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        header = conn.recv(HEADER).decode(FORMAT)  # blocking line

        if not header:
            continue

        msg_len = int(header)
        msg = conn.recv(msg_len).decode(FORMAT)

        if msg == DISCONNECT_MESSAGE:
            connected = False
            break

        print(f"[MESSAGE RECEIVED][{addr}] {msg}")

    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()  # blocking line
        thread = threading.Thread(target=handle_client, args=(conn, addr))

        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting ...")
start()

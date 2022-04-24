#! /usr/bin/env python3
import socket, os, re, sys, threading
sys.path.append("../lib")
import params

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = os.getcwd() + "/server_data"
print(SERVER_DATA_PATH)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    conn.send("OK@Welcome to the File Server".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        print(data)
        data = data.split("@")
        print(data)
        cmd = data[0]

        if cmd == "HELP":
            send_data = "OK@"
            send_data += "LIST: List all the files from the server.\n"
            send_data += "UPLOAD <PATH>: Upload file to the server.\n"
            send_data += "DELETE <filename>: Delete a file from the server.\n"
            send_data += "LOGOUT: Disconnect form the server.\n"
            send_data += "HELP: List all the commands.\n"

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        elif cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            print(files)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty."
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name = data[1]
            text = data[2]

            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

                send_data = "OK@File uploaded."
                conn.send(send_data.encode(FORMAT))
        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    send_data += "File deleted"
                else:
                    send_data += "File not found!"
            conn.send(send_data.encode(FORMAT))

        
    print(f"[DISCONNECTED] {addr} disconnected")



def main():
    switchesVarDefaults = (
        (('-l', "--listenPort"), "listenPort", 50001),
    )

    paramMap = params.parseParams(switchesVarDefaults)

    listenPort = paramMap["listenPort"]
    listenAddr = ''  # Symbolic name meaning all available interfaces

    # Create socket to listen
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind socket to address
    s.bind((listenAddr, listenPort))

    print("[STARTING] Server is starting...")

    # Server is listening, i.e., server is now waiting for the client to connected. (5) connections at most
    s.listen(5)
    print("[LISTENING] Server is listening...")

    while True:
        # Server has accepted the connection from the client.
        conn, addr = s.accept()

        # Creating thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

main()

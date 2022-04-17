#! /usr/bin/env python3
import socket, os, re, sys, threading
sys.path.append("../lib")
import params

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
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
        print(f"[NEW CONNECTION] {addr} connected.")

        # Receiving the filename from the client.
        filename = conn.recv(SIZE).decode(FORMAT)

        # Printing filename to see if it was sent successfully
        print(filename)
        print(f"[RECV] Receiving the filename.")
        file = open(filename, "w")
        conn.send("Filename received!".encode(FORMAT))

        # Receiving the file data from the client.
        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the file data.")
        file.write(data)
        conn.send("File data received!".encode(FORMAT))

        # Closing File.
        file.close()

        # Closing connection form client
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")
main()

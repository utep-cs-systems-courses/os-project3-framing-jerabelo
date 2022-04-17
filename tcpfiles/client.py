#! /usr/bin/env python3
import socket, sys, os, re
sys.path.append("../lib")
import params

IP = socket.gethostbyname(socket.gethostname())
FORMAT = "utf-8"
SIZE = 1024

def archiver(list_of_files):
    byte_array = bytearray()

    for file_name in list_of_files:
        path = "files/" + file_name
        with open(path, "rb") as file:
            tmp_arr = bytearray()
            tmp_arr = file.read()
        byte_array = byte_array + f"{len(tmp_arr):08d}".encode() + tmp_arr
    return byte_array

def main():
    switchesVarDefaults = (
        (('-s', "--server"), "server", "127.0.0.1:50001"),
    )

    paramMap = params.parseParams(switchesVarDefaults)
    server = paramMap["server"]

    try:
        serverHost, serverPort = re.split(':', server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    s = None
    for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res

        # Try creating socket based on above info
        try:
            print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(" error: %s" % msg)
            s = None
            continue
        # Try to connect to remote socket at given address
        try:
            print("attempting to connect to %s" % repr(sa))
            s.connect(sa)
        except socket.error as msg:
            print(" error: %s" % msg)
            s.close()
            s = None
            continue
        break

    if s is None:
        print("Could not open socket")
        sys.exit(1)

    # Open & read the file data.
    file = open("files/txtfile1.txt","r")
    data = file.read()

    # Sending the filename to the server.
    s.send("txtfile1.txt".encode(FORMAT))
    msg = s.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    s.send(data.encode(FORMAT))
    msg = s.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    # Closing file & closing connection to erver
    file.close()
    s.close()


main()
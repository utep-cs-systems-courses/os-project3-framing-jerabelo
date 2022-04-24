#! /usr/bin/env python3
import socket, sys, os, re
sys.path.append("../lib")
import params

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
FORMAT = "utf-8"
SIZE = 1024

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

    while True:
        data = s.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            s.send(cmd.encode(FORMAT))
            # Closing down the thread
        elif cmd == "LOGOUT":
            s.send(cmd.encode(FORMAT))
            break
        elif cmd == "LIST":
            s.send(cmd.encode(FORMAT))

        elif cmd == "UPLOAD":
            ## UPLOAD@filename@textdata
            path = data[1]
            with open(f"{path}", "r") as f:
                text = f.read()
            ## files/data.txt
            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            s.send(send_data.encode(FORMAT))
            pass
        elif cmd == "DELETE":
            s.send(f"{cmd}@{data[1]}".encode(FORMAT))


    print("Disconnected from the server")
    s.close()
main()
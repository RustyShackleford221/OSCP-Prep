import sys, socket, threading, argparse

def request_handler(buff):
    # perform the necesary packet modifications
    return buff

def response_handler(buff):
    # perform the necessary packet modifications
    return buff

def receive_from(connection):
    buff = "".encode()

    # setting a 2 second timeout
    connection.settimeout(2)

    try:
        # keep reading into the buffer until no more data left or timeout
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buff += data
    except:
        pass
    return buff


def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X".encode() % (digits, ord(x)) for x in s])
        text = b''.join([x.encode() if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text))

    print(b'\n'.join(result))

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # connect to remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receieve data from remote if necessary
    if receive_first:
        remote_buff = receive_from(remote_socket)

        remote_buff = response_handler(remote_buff)

        # if there is data to send to the local client, do it
        if len(remote_buff):
            print("[<==] Sending {0} bytes to local_host".format(len(remote_buff)))
            client_socket.send(remote_buff)

    # loop: read from local, send to remote, send to local
    while True:
        # read from local_host
        local_buff = receive_from(client_socket)


        if len(local_buff):
            print("[==>] Received {0} bytes from local_host", len(local_buff))
            hexdump(local_buff.decode(errors="ignore"))

            # send local buffer to request handler
            local_buff = request_handler(local_buff)

            # send data to remote host
            remote_socket.send(local_buff)
            print("[==>] Sent to remote.")

            # receive back the response
            remote_buff = receive_from(remote_socket)

        if len(remote_buff):
            print("[<==] Received {0} bytes from remote".format(len(remote_buff)))
            hexdump(remote_buff.decode(errors="ignore"))

            # send the data to the resposne handler
            remote_buff = response_handler(remote_buff)

            # send respose back to the local socket
            client_socket.send(remote_buff)

            print("[<==] Sent to localhost.")

        # if no more data on either side, close the connections
        if not len(local_buff) or not len(remote_buff):
            client_socket.close() 
            remote_socket.close()
            print("[*] No more data. Closing connections.") 
            
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen in {0}:{1}".format(local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissons.")
        sys.exit(0)
    
    print("[*] Listening on {0}:{1}".format(local_host, local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print hte local connection info
        print("[==>] Received incoming connection from {0}:{1}".format(addr[0], addr[1]))

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

def main():
    parser = argparse.ArgumentParser(description="a simple TCP proxy tool")
    parser.add_argument("local_host", type=str)
    parser.add_argument("local_port", type=int)
    parser.add_argument("remote_host", type=str)
    parser.add_argument("remote_port", type=int)
    parser.add_argument("receive_first", type=str)
    args = parser.parse_args()

    receive_first = True if "True" in args.receive_first else False

    # spin up the listening socket
    server_loop(args.local_host, args.local_port, args.remote_host, args.remote_port, receive_first)

main()

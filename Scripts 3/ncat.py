import sys, socket, getopt, threading, subprocess, argparse

# globals (used for options)
listen = False
command = False
upload = None
execute = None
target = None
upload_destination = None
port = None

def main():
    global target
    global port
    global listen
    global execute
    global command
    global upload_destination

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Simple ncat clone.")
    parser.add_argument("port", type=int, help="target port")
    parser.add_argument("-t", "--target_host", type=str, help="target host", default="0.0.0.0")
    parser.add_argument("-l", "--listen", help="listen on [host]:[port] for incomming connections", action="store_true", default=False)
    parser.add_argument("-e", "--execute", help="--execute=file_to_run execute the given file upn receiving a connection")
    parser.add_argument("-c", "--command", help="initialize a command shell", action="store_true", default=False)
    parser.add_argument("-u", "--upload", help="--upload=destination upon receing connection upload a file and write to [destination]")
    args = parser.parse_args()

    # parse arguements
    target = args.target_host
    port = args.port
    listen = args.listen
    execute = args.execute
    command = args.command
    upload_destination = args.upload

    # are we goint to listen or just send data from stdin?
    if not listen and target is not None and port > 0:
        print("DBG: read data from stdin")
        # read buffer from stdin, this will block so send CTRL-D if not
        # sending to stdin
        buff = sys.stdin.read()

        print("Sending {0} to client".format(buff))
        # send data off
        client_sender(buff)

    # we are going to listen and potentially upload things, execute
    # commands and drop a shell back, depending on the command line options
    if listen:
        server_loop()

def client_sender(buff):
    print("DBG: sending data to client on port " + str(port))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to target host
        client.connect((target, port))

        if len(buff):
            client.send(buff.encode())
        while True:
            # now let's wait for data response
            recv_len = 1
            response = ""

            while recv_len:
                print("DBG: waiting for response from client")
                data = client.recv(4096) 
                recv_len = len(data)
                response += data.decode(errors="ignore")

                if recv_len < 4096:
                    break

            print(response, end="")

            # wait for more input
            buff = input("")
            buff += "\n"

            # send it off
            client.send(buff.encode())
    except:
        print("[*] Exception! Exiting.")
    finally:
        client.close()

def server_loop():
    global target
    print("DBG: entering server loop")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin a thread to handle the new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    # trim the newline
    command = command.rstrip()
    print("DBG: executing command: " + command)

    try:
        # this will launch a new process, NOTE: cd commands are useless
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute comamnd.\r\n"

    # send the output back to the client
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    print("DBG: handling client socket")

    # check for upload
    if upload_destination is not None:
        print("DBG: entering file upload")
        # read all of the bytes and write them to the destination
        file_buff = ""

        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buff += data.decode()

        # write bytes to file
        try:
            f = open(upload_destination, "wb")
            f.write(file_buff)
            f.close()

            # ACK file writing
            client_socket.send("Successfully saved file to: {0}\r\n".format(upload_destination).encode())
        except:
            client_socket.send("Failed to save file to {0}. Are you sure the directory exists?\r\n".format(upload_destination).encode())

    if execute is not None:
        print("DBG: going to execute command")
        # run the command
        output = run_command(execute)
        client_socket.send(output.encode())

    # go into loop ifa command shell was requested
    if command:
        print("DBG: shell requested")
        # show a prompt
        client_socket.send("<BHP:#> ".encode())
        while True:

            # now recieve until linefeed
            cmd_buff = ""
            while "\n" not in cmd_buff:
                cmd_buff += client_socket.recv(1024).decode()

            # send back the command output
            response = run_command(cmd_buff)

            if isinstance(response, str):
                response = response.encode()

            # send back the response
            client_socket.send(response + "<BHP:#> ".encode())

main()
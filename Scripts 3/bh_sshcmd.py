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
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024).decode())
    
ssh_command(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
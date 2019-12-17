'''
This is a very simple utility to create ssh sessions and do SCP from one system to another.
To create a ssh client, create an object of sshClient type and pass the required information
For scp, appropriate filename and its path would be required.
    The getscp command will always download from remote machine to a local directory
'''

import paramiko
from scp import SCPClient


class sshClient ():
    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # yes
        try:
            self.ssh.connect(self.host, self.port, self.user, pwd)
            self.sshConnStatus = True
        except paramiko.ssh_exception.AuthenticationException:
            self.sshConnStatus = False
            print ('failed login for ', self.host)


    def executeCommand(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        output = stdout.read().decode('ascii')
        return output if output else stderr.read().decode('ascii')    # bytes into unicode


    def ScpGetTransport(self, filename):
        if not self.sshConnStatus:
            print ('SSH connection not established, no SCP possible')
            return
        mscp = SCPClient(self.ssh.get_transport())
        mscp.get(filename)


    def ScpPutTransport(self, filename, filepath):
        if not self.sshConnStatus:
            print ('SSH connection not established, no SCP possible')
            return
        mscp = SCPClient(self.ssh.get_transport())
        mscp.put(filename, filepath)


    def __del__(self):
        self.ssh.close()


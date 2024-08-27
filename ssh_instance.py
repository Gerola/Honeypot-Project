import logging
import socket
import threading
import sys
import paramiko
import time

# The following was referenced in the making of this part of the project:
# https://github.com/paramiko/paramiko/blob/main/demos/demo_server.py
# https://docs.paramiko.org/en/latest/api/server.html


#Logger commands
logger = logging.getLogger('ssh')
logger.setLevel(logging.INFO)
ch = logging.FileHandler('./Logs/SSHLogsCommands.txt',mode='a')
ch.setLevel(logging.INFO)
forma = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(forma)
logger.addHandler(ch)

#Logger for login attempts
logger2 = logging.getLogger('sshUserPass')
logger2.setLevel(logging.INFO)
ch2 = logging.FileHandler('./Logs/SSHLogsUserPass.txt',mode='a')
ch2.setLevel(logging.INFO)
forma2 = logging.Formatter('%(asctime)s - %(message)s')
ch2.setFormatter(forma2)
logger2.addHandler(ch2)


#Messages and Keys
host_key = paramiko.RSAKey(filename='id_rsa')#Need to make this on own side
OS_MESSAGE = b"Welcome to Ubuntu 20.04.6 LTS (GNU/Linux)\n\n\r"
WELCOMING_MESSAGE = b"Welcome to the SSH server\n\n\r"
COMMAND_LINE = b"user@Ubuntu:~/home/user/important$ "


#Class
class Server(paramiko.ServerInterface):
    def __init__(self,username,password):#Set the username and password
        self.event = threading.Event()
        self.username = username
        self.password = password

    def check_channel_request(self,kind,chid):#What kind of session
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        else:
            return paramiko.OPEN_FAILED_CONNECT_FAILED
    
    def get_allowed_auths(self,username):#How to connect
        return "password"
    
    def check_auth_none(self,username):
        return paramiko.AUTH_FAILED

    def check_auth_password(self, username, password):#Check password and username, as well as log
        logger2.info(f"Username: { username } Password: { password }")
        if (username == self.username) and (password == self.password):
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED
    
    def check_channel_shell_request(self, channel):#if a shell or shell environment is provided
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):#terminal given or not
        return True

#Convince the client
def shell_environment(channel,IP):
    channel.send(OS_MESSAGE)
    channel.send(WELCOMING_MESSAGE)
    channel.send(COMMAND_LINE)
    commands = b''
    while(True):  #Support commands
        a = channel.recv(1)
        commands = commands + a
        channel.send(a)
        if a == b'\r':
            channel.send("\n")

            time.sleep(1)
            if commands == b'ls\r':
                channel.send(b"adminCreds website.creds Notes.txt\n\r")
                logger.info(f"IP: {IP} command: ls ")

            elif commands == b'uname\r':
                channel.send(b"Linux\n\r")
                logger.info(f"IP: {IP} command: uname ")

            
            elif commands == b'pwd\r':
                channel.send(b"/home/user/important\n\r")
                logger.info(f"IP: {IP} command: pwd ")


            elif commands == b'cat adminCreds\r':
                channel.send(b"Username: admin123 password: ddaea25b73c47cb93c83407619f048b8545f401ff40ffbbbc58c786daa3bc5bb \n\r")
                logger.info(f"IP: {IP} command: cat adminCreds ")

            
            elif commands == b'cat website.creds\r':
                channel.send(b"Username: webmin password: ae42aca575c15623c907cd92ea7ea8f668d2f912dda586ad7d541d147d00066f \n\r")
                logger.info(f"IP: {IP} command: cat website.creds ")

            
            elif commands == b'cat Notes.txt\r':
                channel.send(b"Change default credentials from ssh and rework parts of the system to be more secure. \n\r")
                logger.info(f"IP: {IP} command: cat Notes.txt ")

            
            elif commands == b'exit\r':
                channel.send(b"Bye! :)\n\r")
                logger.info(f"IP: {IP} command: exit")
                channel.close()
                return

            elif len(commands) > 1:
                channel.send(str(commands)[2:-3])
                com = str(commands)[2:-3]
                channel.send(b": command not found\n\r")
                logger.info(f"IP: {IP} command: [{com}")


            commands = b''
            channel.send(COMMAND_LINE)

        elif a == b'\x03': # control + C
            channel.close()
            return


# Threading to handle the clients to allow multiple clients connecting to the honeypot
def handle_clients(client,IP,username,password):
    try:
        t = paramiko.Transport(client)#Get a transport object with the client socket
        server = Server(username,password)#make a server object

        t.add_server_key(host_key)#add the server key
        t.start_server(server=server)#start the server with the server object
    
        channel = t.accept(100)
        if channel == None:
            sys.exit()
        server.event.wait(15)#wait for a certain amount of time 
        if not server.event.is_set():#if not set, which would be the shell request setting it then exit
            sys.exit(1)

        shell_environment(channel,IP)#start the emulated shell to try and trick the client

    except:
        # print("Error in setting up the environment")
        pass

    finally:#close everything when done
        try:
            t.close()
            channel.close()
            client.close()
        except:
            pass
            
    
#run the ssh
def ssh(port=9999,username="admin",password="admin"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("",port))
    sock.listen()
    
    while(True):
        client,addr = sock.accept()#accept then start the thread and wrap back around
        honeypot = threading.Thread(target=handle_clients,args=(client,addr[0],username,password,))
        honeypot.start()
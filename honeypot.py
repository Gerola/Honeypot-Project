from website_instance import run_website
from ssh_instance import ssh
from plotResults import plot_data
import argparse

parser = argparse.ArgumentParser(description="Arguments to customize the program to the user's preference")

    #Plot results:
parser.add_argument('-o','--plot',metavar="Plot results",type=int,default=0,help="If the user wants the results to be plotted and saved to a PDF")

    # HTTP Flags:
parser.add_argument('-hp','--HTTPport',metavar="HTTP Port",type=int,default=8080,help="What port the server should be listening on.")
parser.add_argument('-t','--HTTP',metavar="HTTP Mode",type=int,default=0,help="Run as HTTP Honeypot, set as -t 1")
   
    # SSH Flags:
parser.add_argument('-s','--SSH',metavar="SSH Mode",type=int,default=0,help="Run as SSH Honeypot, set as -s 1")
parser.add_argument('-sp','--SSHport',metavar="SSH Port",type=int,default=9999,help="What port the server should be listening on.")
parser.add_argument('-u','--username',metavar="SSH Username",type=str,default="admin",help="What the username of the SSH account should be")
parser.add_argument('-p','--password',metavar="SSH Password",type=str,default="admin",help="What the password of the SSH account should be")

    # Interactive or not:
parser.add_argument('-i','--interactive',metavar="Interactive",type=int,default=0,help="Have the setup be interactive set as -i 1")

#Interactive setup
def interactive_setup():
    http_or_ssh = 0
    port = 0
    username = ""
    password = ""
    
    while(http_or_ssh != '1' and http_or_ssh != '0'):
        http_or_ssh = input("What honeypot do you want to run?\n(0) HTTP\n(1) SSH\n")
    
    if http_or_ssh == '0':
        while(int(port) < 20 or int(port) > 65000):
            port = input("What port do you want the server to run on? (80 default)\n")
        run_website(port)
    elif http_or_ssh == '1':
        while(int(port) < 20 or int(port) > 65000):
            port = input("What port do you want the server to run on? (22 default)\n")
        while(username == ""):
            username = input("What do you want the username to be?: ")
        while(password == ""):
            password = input("What do you want the password to be?: ")
        ssh(int(port),username,password)

def selection():
    args = parser.parse_args()
    if args.plot == 1:
        plot_data()
        return
    elif args.interactive == 1:
        interactive_setup()
    elif args.HTTP == 0:
        if args.SSH == 0:
            print("Please choose a honeypot")
        else:
            ssh(args.SSHport,args.username,args.password)
    elif args.SSH != 0:
        print("Please choose one honeypot")
    else:
        run_website(args.HTTPport)

if __name__ == '__main__':
    selection()


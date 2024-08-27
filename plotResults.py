import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages 
import re

#Holds all the data collected from the honeypots
ssh_Commands = {}
ssh_IP = {}
ssh_User = {}
ssh_Pass = {}
website_Username = {}
website_Password = {}
website_IP = {}
website_email = {}


def read_files():

    #Username and Password pairs used to try and access the ssh server
    try:
        with open("./Logs/SSHLogsUserPass.txt",'r') as sup:
            a = sup.readlines()
            for x in a:
                data = x.strip().split(' ')
                if ssh_User.get(data[4]) == None:
                    ssh_User[data[4]] = 1
                else:
                    ssh_User[data[4]] += 1  
                if ssh_Pass.get(data[6]) == None:
                    ssh_Pass[data[6]] = 1
                else:
                    ssh_Pass[data[6]] += 1
    except:
        print("Unable to process SSHLogsUserPass file, check to make sure formatted correctly.")

    #Commands and the IP used on the ssh server
    try:
        with open("./Logs/SSHLogsCommands.txt",'r') as slc:
            a = slc.readlines()
            for x in a:
                data = x.strip().split(' ')
                if ssh_IP.get(data[4]) == None:
                    ssh_IP[data[4]] = 1
                else:
                    ssh_IP[data[4]] += 1   
                if ssh_Commands.get(data[6]) == None:
                    ssh_Commands[data[6]] = 1
                else:
                    ssh_Commands[data[6]] += 1
    except:
        print("Unable to process SSHLogsCommands file, check to make sure formatted correctly.")
    
        #Get all the data from the website honeypot
    try:
        with open("./Logs/websiteLogs.txt",'r') as sup:
            a = sup.readlines()
            for x in a:
                data = x.strip().split(" ")
                if data[3] == "Register":
                    if website_email.get(data[6]) == None:
                        website_email[data[6]] = 1
                    else:
                        website_email[data[6]] += 1
                    
                    if website_Username.get(data[8]) == None:
                        website_Username[data[8]] = 1
                    else:
                        website_Username[data[8]] += 1

                    if website_Password.get(data[10]) == None:
                        website_Password[data[10]] = 1
                    else:
                        website_Password[data[10]] += 1

                    if website_IP.get(data[12]) == None:
                        website_IP[data[12]] = 1
                    else:
                        website_IP[data[12]] += 1
                else:
                    
                    if website_Username.get(data[6]) == None:
                        website_Username[data[6]] = 1
                    else:
                        website_Username[data[6]] += 1

                    if website_Password.get(data[8]) == None:
                        website_Password[data[8]] = 1
                    else:
                        website_Password[data[8]] += 1

                    if website_IP.get(data[10]) == None:
                        website_IP[data[10]] = 1
                    else:
                        website_IP[data[10]] += 1
    except:
        print("Unable to process websiteLogs file, check to make sure formatted correctly.")                    


def arrange_data(name="N/A",what="N/A",data={}):
    try:
        sort = lambda x: x[1]
        s = sorted(data.items(),key=sort,reverse=True)
        c = [x[1] for x in s]
        p = [re.sub('[^A-Za-z0-9@\.]*','',x[0]) for x in s]
        f = plt.figure(figsize = (12,7))
        plt.xlabel(what)
        plt.ylabel("Number of times")
        plt.title(f"Top 10 {what} on the {name} server")
        plt.bar(p[0:11],c[0:11],color='deepskyblue',width=0.4)
    except:
        print("Error while making graph(s)")


#Only the top ten
def plot_data():
    file = "Data_Collected.pdf"
    p = PdfPages(file)
    read_files()
    if ssh_Commands != {}:
        arrange_data("SSH","Commands",ssh_Commands) #work
    if ssh_User != {}:
       arrange_data("SSH","Users",ssh_User) #work
    if ssh_Pass != {}:
        arrange_data("SSH","Passwords",ssh_Pass) #work
    if ssh_IP != {}:
        arrange_data("SSH","IP",ssh_IP) #work
    if website_email != {}:
        arrange_data("Website","Email",website_email) #work
    if website_IP != {}:
        arrange_data("Website","IP",website_IP) #work
    if website_Username != {}:
        arrange_data("Website","Users",website_Username) #work
    if website_Password != {}:
        arrange_data("Website","Password",website_Password)#work


    try:
        #Get all the figures numbers
        t = plt.get_fignums()

        #Get a reference to the figures
        figs = [plt.figure(x) for x in t]
        
        #Save the figures with the Pdf Pages
        for x in figs:
            p.savefig(x)
        
        #Close the file
        p.close()
    except:
        print("Error while saving files to PDF")
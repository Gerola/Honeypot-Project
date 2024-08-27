# Honeypot
This is a honeypot project that supports the following protocols.
- SSH
- HTTP
- Potentially more in the Future

## Run Interactive
For the honeypot to be run interactive, which means the user will give it information as you go. Run the following command ` python3 honeypot.py -i 1 `. With this command it will go through the steps needed to setup the honeypot in either HTTP or SSH mode. It will guide you through the steps and what needs to be supplied for the setup to succeed.


## Run as SSH with arguments
To Run ` python3 honeypot.py -SSH ` <br><br>
The SSH part of the honeypot should start when the above command is executed, given everything is installed and configured. The message <insertMessage> should display on the terminal when the honeypot starts successfully. It will log usernames and passwords attempted in one log file titled <insertName>, while the log file <insertName> will log the commands executed by a user when they successfully authenticate with the server.

## Run as HTTP with arguments
To Run ` python3 honeypot.py -HTTP ` <br><br>
The HTTP part of the honeypot should have two pages available when started. The login and registration page. It should default to the login page when going to the webpage. When data is entered and submitted for either page, the data submitted will be written to the text file {insertNameFile}. It will log the username, password, IP, time and for the registration page the email the client entered.

## Troubleshooting
- Be sure the install the required libraries from the requirements.txt file with ` pip3 install -r <path to file> `
- If using a port below 1024 you need to use ` sudo ` because all those are privileged ports. Which HTTP (80) and SSH (22) ports are
- Create a key with the command ` ssh-keygen -t rsa ` to have the server operate correctly when run in SSH mode

## Convert Data to PDF File
After data is collected from the honeypots run the command ` python3 honeypot -o 1 ` to get the pdf file with the graphs generated from the available data.

## Disclaimer
- The author is not responsible for anything that happens when running this honeypot. Use for **educational** and **legal** purposes only.

# Honeypot (In Progress)

This is a honeypot project that supports the following protocols.
- SSH
- HTTP
- Potentially more in the Future

## Run as SSH
N/A
## Run as HTTP
To Run ` python3 insert_command ` <br><br>
The HTTP part of the honeypot should have two pages available when started. The login and registration page. It should default to the login page when going to the webpage. When data is entered and submitted for either page, the data submitted will be written to the text file {insertNameFile}. It will log the username, password, IP, time and for the registration page the email the client entered.
## Troubleshooting
- Be sure the install the required libraries from the requirements.txt file with ` pip3 install -r <path to file> `.
- If using a port below 1024 you need to use ` sudo ` because all those are privileged ports. Which HTTP (80) and SSH (22) ports are.
- Create a key with the command ` ssh-keygen -t rsa ` to have the server operate correctly.
## Convert Data to PDF
N/A
## Notes
- The author is not responsible for anything that happens when running this honeypot. Use for legal purposes only and at own discretion.

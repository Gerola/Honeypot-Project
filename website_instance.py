from flask import Flask, render_template, request, redirect
import logging
import random
import time


app = Flask(__name__)

#Logger
logger = logging.getLogger('website')
logger.setLevel(logging.INFO)
ch = logging.FileHandler('./Logs/websiteLogs.txt',mode='a')
ch.setLevel(logging.INFO)
forma = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(forma)
logger.addHandler(ch)

#Redirect to the login page
@app.route('/')
def homepage():
    return redirect("/login")

#Login page
@app.route('/login',methods=['GET','POST'])
def login():
    a = random.randint(0,1)
    if request.method == 'GET':
        return render_template('login.html',message="")
    else:
        user = request.form["username"]
        paswd = request.form["password"]
        IP = request.remote_addr
        time.sleep(5) #Sleep to create more problems and limit the enumeration possiblity
        logger.info(f"Login --> Username: {user} Password: {paswd} IP: {IP}")
        if a == 0:#Random about what to say to the user
            return render_template('login.html', message="Invalid Username")
        else:
            return render_template('login.html', message="Incorrect Password")

#Register an account
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html',message="")
    else:
        user = request.form["username"]
        paswd = request.form["password"]
        email = request.form["email"]
        IP = request.remote_addr
        logger.info(f"Register --> Email: {email} Username: {user} Password: {paswd} IP: {IP}")
        return render_template('register.html',message="Thank You for Registering. Please go to Login to continue.")

#Run the website
def run_website(wanted_port=8080):
    app.run(port=wanted_port)

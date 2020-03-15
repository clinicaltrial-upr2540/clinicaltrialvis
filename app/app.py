from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)

############################################
# Startup tasks go here (load/check data)
############################################



############################################
# Routes to web pages go here
############################################

# Route to homepage
@app.route("/")
def index():
	return render_template('home.html')

@app.route("/test")
def test():
	return render_template('test.html')

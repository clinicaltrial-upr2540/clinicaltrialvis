from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('home.html')
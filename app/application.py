from flask import Flask, render_template, session, redirect, request

@app.route("/")
def index():
	return render_template('home.html')
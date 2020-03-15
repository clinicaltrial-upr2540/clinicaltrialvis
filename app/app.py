from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
application = Flask(__name__)

app = Flask(__name__)
app.config['TESTING'] = True

############################################
# Startup tasks go here (load/check data)
############################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com/drugdata'
db = SQLAlchemy(application)

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

if __name__ == "__main__":
	app.run(debug=True)
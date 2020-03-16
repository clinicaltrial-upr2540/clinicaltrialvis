from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
application = Flask(__name__)

app = Flask(__name__)
app.config['TESTING'] = True

if __name__ == "__main__":
	app.run(debug=True)

############################################
# Startup tasks go here (load/check data)
############################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com/drugdata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

############################################
# Routes to web pages go here
############################################

# Route to homepage
@app.route("/")
def index():
	print(db)
	return render_template('home.html', db=db)

@app.route("/test")
def test():
	return render_template('test.html')


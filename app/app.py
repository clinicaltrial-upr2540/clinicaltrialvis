#!/usr/bin/env python3

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TESTING'] = True

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
def render_index():
    print(db)
    return render_template('home.html', page_title="Home")


@app.route("/test")
def render_test():
    return render_template('test.html', page_title="Test Page")


@app.route("/visualizations")
def render_visualizations():
    return render_template('visualizations.html', page_title="Visualizations")


if __name__ == "__main__":
    app.run(debug=True)
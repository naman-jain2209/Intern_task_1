from flask import Flask, redirect, url_for, render_template,request
from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import text, create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from Data_fetching import data_fetch, write_file, preprocess
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
passwd=os.getenv('DB_Password')
db_name='db'
# Getting Data from NewsAPI
# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the MYSQL database, relative to the app instance folder
connection_str = "mysql+mysqlconnector://root:"+passwd+"@"+db_name+":3306/intern_task"
app.config['SQLALCHEMY_DATABASE_URI']=connection_str
# initialize the app with the extension
engine=create_engine("mysql+mysqlconnector://root:"+passwd+"@"+db_name+":3306/intern_task")
db = SQLAlchemy(app)


@app.route("/", methods=['POST', 'GET'])
def xyz():
    return render_template('First.html')

@app.route("/enter", methods=['POST', 'GET'])
def enter():
    if request.method=='POST':
        x=str(request.form['topic']) 
        y=str(request.form['start_date'])
        z=str(request.form['end_date'])
    data_fetch(x,y,z)
    title= "News for Topic "+x+" From "+y+" to "+z+'.'
    dates = db.session.execute(text('select distinct(Dates) from News;')).scalars()
    dates=list(dates)
    return render_template('Second_Page.html',title=title, Dates=map(json.dumps, dates))

@app.route("/submit",methods=['POST', 'GET'])
def submit():
    if request.method=='POST':
        x=str(request.form['dropdown1'])
        x=x[1:-1]
        y=request.form['dropdown2']
    title="Resultant Links for Date="+x+" and Sentiment="+y
    links= db.session.execute(text('select url from News where Dates=:X and Sentiment=:Y;'), {"X":x, "Y":y}).scalars()
    # links=pd.read_sql('select url from News where Dates='+x+' and Sentiment='+y+';',engine)
    return render_template('Result.html',title=title, Links=map(json.dumps, links))
    

if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
from flask import Flask, render_template, request
import openpyxl
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv
import json
import socket
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('transcript.html')

@app.route('/', methods=['POST'])
def getvalue():
    issue= request.form['type']
    age= request.form['age']
    lvl= request.form['dangerlvl']
    story=request.form['text']
    hostname = socket.gethostname()    
    ip = socket.gethostbyname(hostname) 
    print(ip)
    print(issue)
    print(age)
    print(lvl)    
    print(story)   
    full= "The Issue is: " + issue + "The person's age is :" + age + "The danger level from 1-10 is: " + age + " The full story is: " + story  
    with  open("db.csv","a")as file:
        writer = csv.writer(file)
        writer = csv.writer(file)
        writer.writerow([issue , age, lvl, story,ip])               
        print(file)
        file.close()
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)
    sheet = client.open("Data_Center").sheet1  # Open the spreadhseet
    content = open('db.csv', 'r').read()

    client.import_csv('14lUAqaMihPWx6LKM0pfALLph9tMNJ3R5nXV11d9sE64', content)

    data = sheet.get_all_records()  # Get a list of all records
    print (data)    


    return render_template("end.html")  





if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import sqlite3
import datetime

app=Flask(__name__)

@app.route('/')
def home():
    #fetch divisional points and determine the total per division and order them
    first=['north',0]; second=['north',0]; third=['north',0]; north=['North',0]; south=['South',0]; west=['West',0]
    with sqlite3.connect("db/Divisionalpoints.db") as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT colour,name FROM Divisions")
        results=cursor.fetchall()
        #fetch and list the colour and name for each division
        for result in results:
            if result[1]=='north':
                north.append(result[0])
            if result[1]=='south':
                south.append(result[0])
            if result[1]=='west':
                west.append(result[0])
        cursor.execute("SELECT north, south, west FROM Points")
        thing=cursor.fetchall()
        #add all the points for each event to find total per division
        for item in thing:
            north[1]=north[1]+item[0]; south[1]=south[1]+item[1]; west[1]=west[1]+item[2]
        divisions=[north,south,west]
        #find the division with the most points
        for division in divisions:
            if division[1]>first[1]:
                first=division
        divisions.remove(first)
        #find the second place division
        for division in divisions:
            if division[1]>second[1]:
                second=division
        divisions.remove(second)
        #the last division=third
        for division in divisions:
            third=division
        #define division values, name and colour eg.num1=largest number, name3=name of div with least points etc.
        num1=first[1]; num2=second[1]; num3=third[1]; name1=first[0]; name2=second[0]; name3=third[0]; col1=first[2]; col2=second[2]; col3=third[2]
        return render_template('home.html', num1=num1,num2=num2,num3=num3,name1=name1,name2=name2,name3=name3,col1=col1,col2=col2,col3=col3)

@app.route('/clubs')
#create a page displaying the clubs
def clubs():
    return render_template("clubs.html")

@app.route('/divpoints',methods=['POST','GET'])
def divpoints():
    if request.method=='POST':
        idk=request.form['North']
        print(idk)
    with sqlite3.connect("db/Divisionalpoints.db") as connection:
        #fetch divisional points by event from sql and display as results in html
        cursor=connection.cursor()
        cursor.execute('SELECT north,south,west,event,date FROM Points ORDER BY date DESC')
        results=cursor.fetchall()
        date=datetime.date.today()
    return render_template('divisionalpoints.html',results=results,date=date)

if __name__=="__main__":
    app.run(debug=True)
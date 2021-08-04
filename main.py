from flask import Flask, flash, render_template, request, redirect
import sqlite3
import datetime

from flask.helpers import url_for

app=Flask(__name__)

def connectsql(data,query):
    with sqlite3.connect(data) as connection:
        cursor=connection.cursor()
        cursor.execute(query)
        results=cursor.fetchall()
        return results

def check(value):
    try:
        value=int(value)
        if value>=0:
            return True
        else:
            return False
    except:
        return False



week1=datetime.datetime.now().strftime("%W")
week=int(week1)
if (week%2) ==0:
    week='B'
else:
    week='A'
date=datetime.datetime.now().strftime("%d/%m/%Y")
datet=datetime.datetime.now().strftime("%Y-%m-%d")
@app.route('/')
def home():
    #fetch divisional points and determine the total per division and order them
    first=['north',0]; second=['north',0]; third=['north',0]; north=['North',0]; south=['South',0]; west=['West',0]
    results=connectsql("db/Divisionalpoints.db","SELECT colour,name FROM Divisions")
        #fetch and list the colour and name for each division
    for result in results:
        if result[1]=='north':
            north.append(result[0])
        if result[1]=='south':
            south.append(result[0])
        if result[1]=='west':
            west.append(result[0])
    thing=connectsql("db/Divisionalpoints.db","SELECT north, south, west FROM Points")
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
    contents=connectsql("db/HomePageContent.db","SELECT content,colour,image,width,height,link,target FROM Content ORDER BY box")
    content=[]
    for item in contents:
        if item[2]!=None:
            item=list(item)
            item[3]=item[3]+2
            item[4]=item[4]+2
            item=tuple(item)
        content.append(item)
    return render_template('home.html', num1=num1,num2=num2,num3=num3,name1=name1,name2=name2,name3=name3,col1=col1,col2=col2,col3=col3,content=content,week=week,date=date)

@app.route('/clubs', methods=['POST','GET'])
#create a page displaying the clubs
def clubs():
    with sqlite3.connect("db/Clubs.db") as connection:
        if request.method=='POST':
            categories=request.form['categories']
            if categories=='0':
                cursor=connection.cursor()
                cursor.execute('SELECT Club.title,Club.room,Club."desc",Club.contact,Club.teachcode,Club.category,club.restrictions FROM Club')
                clubs=cursor.fetchall()
            else:
                clubs=[]
                cursor=connection.cursor()
                cursor.execute('SELECT COUNT(id)FROM Club')
                amount=cursor.fetchall()
                for item in amount:
                    for x in range(item[0]):
                        x1=x+1
                        query='SELECT Club.title,Club.room,Club."desc",Club.contact,Club.teachcode,Club.category,club.restrictions FROM Club WHERE id=?'
                        cursor.execute(query,(x1,))
                        fetch=cursor.fetchall()
                        for category in fetch:
                            cat=int(category[5])
                            categories=int(categories)
                            if cat==categories:
                                clubs.append(category)
        else:
            cursor=connection.cursor()
            cursor.execute('SELECT Club.title,Club.room,Club."desc",Club.contact,Club.teachcode,Club.category,club.restrictions FROM Club')
            clubs=cursor.fetchall()
    return render_template("clubs.html",clubs=clubs,week=week,date=date)


@app.route('/divpoints',methods=['POST','GET'])
def divpoints():
    error=None
    if request.method=='POST':
        password=request.form['Password']
        if password=='Bottleofwater43':
            north=request.form['North']
            if check(north)==True:
                south=request.form['South']
                if check(south)==True:
                    west=request.form['West']
                    if check(west)==True:
                        event=request.form['Event']
                        error='Divisional Points entry was successful'
                        with sqlite3.connect("db/Divisionalpoints.db") as connection:
                            insert=connection.cursor()
                            query=('INSERT INTO Points(north, south, west, event, date) VALUES (?, ?, ?, ?, ?);')
                            insert.execute(query,(north,south,west,event,datet))
                            return render_template('divisioncodesucessful.html', error=error)
            else:
                error='Invalid Input'
        else:
            error='Invalid Password'

    with sqlite3.connect("db/Divisionalpoints.db") as connection:
        #fetch divisional points by event from sql and display as results in html
        cursor=connection.cursor()
        cursor.execute('SELECT north,south,west,event,date FROM Points ORDER BY date DESC')
        results=cursor.fetchall()
    return render_template('divisionalpoints.html',results=results,week=week,date=date,error=error)

@app.route('/library')
def library():
    return render_template('library.html',week=week,date=date)

@app.route('/links')
def links():
    return render_template('links.html',week=week,date=date)

@app.route('/printing')
def printing():
    return render_template('printing.html',week=week,date=date)


if __name__=="__main__":
    app.run(debug=True)

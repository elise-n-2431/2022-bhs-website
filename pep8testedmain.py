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
    #confirm divpoint values in form are positive
    try:
        value=int(value)
        if value>=0:
            return True
        else:
            return False
    except:
        return False


#set the current time, week and date for the top of the page
week1=datetime.datetime.now().strftime("%W")
week=int(week1)
if (week%2) ==0:
    week='B'
else:
    week='A'
date=datetime.datetime.now().strftime("%d/%m/%Y")
#datet is the date in the format of yyyy-mm-dd for divpoints sql entries
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
    #the remaining division is therefore last
    for division in divisions:
        third=division
    #define division values, name and colour eg.num1=largest number, name3=name of div with least points etc. to display
    num1=first[1]; num2=second[1]; num3=third[1]; name1=first[0]; name2=second[0]; name3=third[0]; col1=first[2]; col2=second[2]; col3=third[2]
    #fetch the box contents for the main page from the database (HomePageContent.db)
    contents=connectsql("db/HomePageContent.db","SELECT content,colour,image,width,height,link,target,iframe FROM Content ORDER BY box")
    content=[]
    for item in contents:
        #if there is an image in the image coloumn, make the dimensions larger as the border will be removed
        if item[2]!=None:
            item=list(item)
            item[3]=item[3]+2
            item[4]=item[4]+2
            item=tuple(item)
        content.append(item)
    #display the home.html page with all of the variables used as their corresponding variables within the page
    return render_template('home.html', num1=num1,num2=num2,num3=num3,name1=name1,name2=name2,name3=name3,col1=col1,col2=col2,col3=col3,content=content,week=week,date=date)

@app.route('/clubs', methods=['POST','GET'])
#create a page displaying the clubs
def clubs():
    with sqlite3.connect("db/Clubs.db") as connection:
        #if the form (categories/time) have any values sumbitted, continue 
        if request.method=='POST':
            #define the variables from the form
            categories=request.form['categories']
            dayvar=request.form['day']
            # if the categories and days have sumbitted 0 (meaning all), select everything
            if categories=='0'and dayvar=='0':
                cursor=connection.cursor()
                cursor.execute('SELECT Club.title,Club.room,Club."desc",Club.contact,Club.teachcode,Club.category,club.restrictions FROM Club ORDER BY Club.title')
                clubs=cursor.fetchall()
            else:
                clubs=[]
                cursor=connection.cursor()
                cursor.execute('SELECT Club.title,Club.room,Club."desc",Club.contact,Club.teachcode,Club.category,club.restrictions,club.id FROM Club ORDER BY Club.title')
                fetch=cursor.fetchall()
                #select all clubs from database
                for club in fetch:
                    if dayvar=='0':
                        #if they selected all days + a category, add all clubs which match the category to a list
                        cat=int(club[5])
                        categories=int(categories)
                        if cat==categories:
                            clubs.append(club)
                        
                    else:
                        #fetch all the entries from the daysclubs table which match the chosen club
                        query='SELECT DaysClubs.daysid FROM DaysClubs JOIN Club ON Club.id=DaysClubs.clubid WHERE Club.id=?'
                        cursor.execute(query,(club[7],))
                        days=cursor.fetchall()
                        for day in days:
                            #for each day which the club is on, check if it matches the day selected by the user
                            dayvar=int(dayvar)
                            day=int(day[0])
                            if day==dayvar:
                                #if the club is on on the selected day, check if the club matches the user's selected category
                                cat=int(club[5])
                                categories=int(categories)
                                if cat==categories:
                                    clubs.append(club)
                                if categories==0:
                                    clubs.append(club)
                                #add to a list if the user selected all categories or the category selected matches the category of the club
        else:
            #select everything from all categories and days from the clubs database
            cursor=connection.cursor()
            cursor.execute('SELECT Club.title,Club.room,Club."desc",Club.contact,Club.teachcode,Club.category,club.restrictions FROM Club')
            clubs=cursor.fetchall()
    #display the clubs page with the list of clubs as the clubs displayed
    return render_template("clubs.html",clubs=clubs,week=week,date=date)


@app.route('/divpoints',methods=['POST','GET'])
def divpoints():
    if request.method=='POST':
        password=request.form['Password']
        passwordconfirm=connectsql("db/Divisionalpoints.db","SELECT password FROM Admin WHERE id=1")
        for passworditem in passwordconfirm:
            if password==passworditem[0]:
                north=request.form['North']
                #only continue if the value>0
                if check(north)==True:
                    south=request.form['South']
                    if check(south)==True:
                        west=request.form['West']
                        if check(west)==True:
                            event=request.form['Event']
                            #change error message to a confirmation of sucess
                            with sqlite3.connect("db/Divisionalpoints.db") as connection:
                                insert=connection.cursor()
                                query=('INSERT INTO Points(north, south, west, event, date) VALUES (?, ?, ?, ?, ?);')
                                insert.execute(query,(north,south,west,event,datet))
                                #insert the values into the divpoints table
                                return render_template('divisioncodesucessful.html')
                else:
                    return render_template('divisioncodefailure.html', error="Invalid Input")
            else:
                return render_template('divisioncodefailure.html', error="Invalid Password")

    with sqlite3.connect("db/Divisionalpoints.db") as connection:
        #fetch divisional points by event from sql and display as results in html
        cursor=connection.cursor()
        cursor.execute('SELECT north,south,west,event,date FROM Points ORDER BY date DESC')
        results=cursor.fetchall()
    return render_template('divisionalpoints.html',results=results,week=week,date=date)

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


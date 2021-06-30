from flask import Flask, render_template, request
import sqlite3
import datetime

app=Flask(__name__)

def connectsql(data,query):
    with sqlite3.connect(data) as connection:
        cursor=connection.cursor()
        cursor.execute(query)
        results=cursor.fetchall()
        return results

@app.route('/')
def home():
    #fetch divisional points and determine the total per division and order them
    first=['north',0]; second=['north',0]; third=['north',0]; north=['North',0]; south=['South',0]; west=['West',0]
    results=connectsql("db/Divisionalpoints.db","SELECT colour,name FROM Divisions")
    '''with sqlite3.connect("db/Divisionalpoints.db") as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT colour,name FROM Divisions")
        results=cursor.fetchall()'''
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
    contents=connectsql("db/HomePageContent.db","SELECT content,size,colour FROM Content ORDER BY box")
    content=[]
    size=[]
    colour=[]
    for item in contents:
        content.append(item[0])
        size.append(item[1])
        colour.append(item[2])
    return render_template('home.html', num1=num1,num2=num2,num3=num3,name1=name1,name2=name2,name3=name3,col1=col1,col2=col2,col3=col3,content=content,size=size,colour=colour)

@app.route('/clubs')
#create a page displaying the clubs
def clubs():
    with sqlite3.connect("db/Clubs.db") as connection:
        cursor=connection.cursor()
        cursor.execute('SELECT Club.title,Club.room,Club."desc",Club.contact,Club.teachcode,Club.category,club.restrictions FROM Club ')
        clubs=cursor.fetchall()
        time='SELECT Time.time FROM Club JOIN ClubTime ON ClubTime.cid=Club.id JOIN Time ON Time.id=ClubTime.tid WHERE Club.id=?;'
        day='SELECT Day.day FROM Club JOIN ClubDay ON ClubDay.cid=Club.id JOIN Day ON Day.id=ClubDay.cid WHERE Club.id=?;'
        '''for club in clubs:
            cursor.execute(time,(club[0],))
            times=cursor.fetchall()
            print(times)
            cursor.execute(day,(club[0],))
            days=cursor.fetchall()
            print(days)'''
        
    return render_template("clubs.html",clubs=clubs)


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

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/links')
def links():
    return render_template('links.html')



if __name__=="__main__":
    app.run(debug=True)
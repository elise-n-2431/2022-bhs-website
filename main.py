from flask import Flask, render_template
import sqlite3

app=Flask(__name__)

@app.route('/')
def home():
    first=0; second=0; third=0; north=0; south=0; west=0
    with sqlite3.connect("db/Divisionalpoints.db") as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT north, south, west FROM Points")
        thing=cursor.fetchall()
        for item in thing:
            north=north+item[0]
            south=south+item[1]
            west=west+item[2]
        divisions=[north,south,west]
        for division in divisions:
            if division>first:
                first=division
        divisions.remove(first)
        for division in divisions:
            if division>second:
                second=division
        divisions.remove(second)
        for division in divisions:
            third=division
    one=first; two=second; three=third; first=first[0]; second=second[0];third=third[0]
    return render_template('home.html', first=first,second=second,third=third,one=one,two=two,three=three)

@app.route('/clubs')
def clubs():
    return render_template("clubs.html")

@app.route('/divpoints')
def divpoints():
    with sqlite3.connect("db/Divisionalpoints.db") as connection:
    #this page is to show the history of all the divisional points as a list and should include a form to add more points hidden behind a login wall. (students shouldn't be able to get in through inspect elements)
        cursor=connection.cursor()
        cursor.execute('')
    return render_template('divisionalpoints.html')

if __name__=="__main__":
    app.run(debug=True)
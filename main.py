from flask import Flask, render_template
import sqlite3

app=Flask(__name__)

@app.route('/')
def home():
    first=('test1',0)
    second=('test1',0)
    third=('test1',0)
    with sqlite3.connect("db/Divisionalpoints.db") as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT division,value FROM test")
        thing=cursor.fetchall()
        for item in thing:
            if item[1]>first[1]:
                first=item
        thing.remove(first)
        for item in thing:
            if item[1]>second[1]:
                second=item
        thing.remove(second)
        for item in thing:
            third=item
        one=first[1]
        two=second[1]
        three=third[1]
        first=first[0]
        second=second[0]
        third=third[0]
    return render_template('home.html', first=first,second=second,third=third,one=one,two=two,three=three)

@app.route('/clubs')
def clubs():
    return render_template("clubs.html")

if __name__=="__main__":
    app.run(debug=True)
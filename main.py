from flask import Flask, render_template
import sqlite3
largest=('test1',0)
with sqlite3.connect("db/Divisionalpoints.db") as connection:
    cursor=connection.cursor()
    cursor.execute("SELECT division,value FROM test")
    thing=cursor.fetchall()
    print(thing)
    for item in thing:
        if item[1]>largest[1]:
            largest=item
    print(f"The winner is: {largest[0]} with {largest[1]} points")
    cursor.execute("UPDATE test SET value=150 WHERE division='South'")
    connection.commit()


app=Flask(__name__)

'''DATABASE = 'db/School.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db'''

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/clubs')
def clubs():
    return render_template("clubs.html")

#hi

if __name__=="__main__":
    app.run(debug=True)
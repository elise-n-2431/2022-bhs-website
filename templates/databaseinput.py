#input 50 entries to Points sql table to test scrolling
x=1
while x<50:
    import sqlite3
    with sqlite3.connect("db/Divisionalpoints.db") as connection:
        cursor=connection.cursor()
        cursor.execute("INSERT INTO Points (north,south,west,event,date) VALUES (100,100,100,'test',2021-05-31)")
        print(x)
        x=x+1
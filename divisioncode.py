import sqlite3
first=('test1',0)
second=('test1',0)
third=('test1',0)
north=0
south=0
west=0
divisions=[north,south,west]
with sqlite3.connect("db/Divisionalpoints.db") as connection:
    cursor=connection.cursor()
    cursor.execute("SELECT north, south, west FROM Points")
    #won't work as database has changed. Need to include something to total all values in each column for the total
    thing=cursor.fetchall()
    for item in thing:
        north=north+item[0]
        south=south+item[1]
        west=west+item[2]
    print(north)
    print(south)
    print(west)
    for division in divisions:
    if item[1]>first[1]:
        first=item
    thing.remove(first)
    for item in thing:
        if item[1]>second[1]:
            second=item
    thing.remove(second)
    for item in thing:
        third=item
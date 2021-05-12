import sqlite3
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
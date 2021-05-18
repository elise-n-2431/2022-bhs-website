import sqlite3
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
        cursor.execute("SELECT ")
    one=first; two=second; three=third; first=first[0]; second=second[0];third=third[0]
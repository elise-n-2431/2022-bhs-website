import sqlite3
first=['north',0]; second=['north',0]; third=['north',0]; north=['north',0]; south=['south',0]; west=['west',0]
with sqlite3.connect("db/Divisionalpoints.db") as connection:
    cursor=connection.cursor()
    cursor.execute("SELECT colour,name FROM Divisions")
    results=cursor.fetchall()
    for result in results:
        if result[1]=='north':
            north.append(result[0])
        if result[1]=='south':
            south.append(result[0])
        if result[1]=='west':
            west.append(result[0])
    cursor.execute("SELECT north, south, west FROM Points")
    thing=cursor.fetchall()
    for item in thing:
        north[1]=north[1]+item[0]
        south[1]=south[1]+item[1]
        west[1]=west[1]+item[2]
    divisions=[north,south,west]
    for division in divisions:
        if division[1]>first[1]:
            first=division
    divisions.remove(first)
    for division in divisions:
        if division>second:
            second=division
    divisions.remove(second)
    for division in divisions:
        third=division
    num1=first[1]; num2=second[1]; num3=third[1]; name1=first[0]; name2=second[0]; name3=third[0]; col1=first[2]; col2=second[2]; col3=third[2]
import sqlite3
with sqlite3.connect("db/Clubs.db") as connection:
    alltimes={}
    allclubs={}
    cursor=connection.cursor()
    cursor.execute('SELECT Club.id,Club.title,Club.room,Club."desc",Club.teacher,Club.teachcode,Club.cost,Categories.type FROM Club JOIN Categories ON Categories.id=Club.category')
    clubs=cursor.fetchall()
    time='SELECT Time.time FROM Club JOIN ClubTime ON ClubTime.cid=Club.id JOIN Time ON Time.id=ClubTime.tid WHERE Club.id=?;'
    day='SELECT Day.day FROM Club JOIN ClubDay ON ClubDay.cid=Club.id JOIN Day ON Day.id=ClubDay.cid WHERE Club.id=?;'
    for club in clubs:
        cursor.execute(time,(club[0],))
        times=cursor.fetchall()
        for time in times:
            club1=[club[0],club[1],club[2],club[3],club[4],club[5],club[6],club[7],time]
            alltimes.update({time:club[0]})
        cursor.execute(day,(club[0],))
        days=cursor.fetchall()
        for day in days:
            allclubs.update({club[0]:day})
    #return render_template(clubs=clubs)
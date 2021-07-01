import sqlite3

def connectsql(data,query):
    with sqlite3.connect(data) as connection:
        cursor=connection.cursor()
        cursor.execute(query)
        results=cursor.fetchall()
        return results


content=connectsql("db/HomePageContent.db","SELECT content,size,colour,image FROM Content ORDER BY box")
print(content)
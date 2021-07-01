import sqlite3

def connectsql(data,query):
    with sqlite3.connect(data) as connection:
        cursor=connection.cursor()
        cursor.execute(query)
        results=cursor.fetchall()
        return results


contents=connectsql("db/HomePageContent.db","SELECT content,colour,image,width,height FROM Content ORDER BY box")
content=[]
for item in contents:
    if item[2]!=None:
        item=list(item)
        item[3]=item[3]+2
        item=tuple(item)
    content.append(item)
print(content)
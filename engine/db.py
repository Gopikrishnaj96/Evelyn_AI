import sqlite3
con =sqlite3.connect("eve.db",check_same_thread=False)
cursor=con.cursor()
query= "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
"""
query="INSERT INTO sys_command VALUES(null,'word','c:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010.lnk')"
cursor.execute(query)
con.commit()
query= "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
query="INSERT INTO web_command VALUES(null,'youtube','https://www.youtube.com/')"
# query="DELETE FROM contacts where id between 3 and 6"
cursor.execute(query)
con.commit() 
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')
query="INSERT INTO contacts (id,'name','mobile_no')VALUES(null,'amma','9447465239')"
cursor.execute(query)
con.commit()
query="INSERT INTO contacts (id,'name','mobile_no')VALUES(null,'aaron','8921042913')"
cursor.execute(query)
con.commit()"""
#query='aaron'
#query=query.strip().lower()
#cursor.execute("SELECT mobile_no FROM contacts   ")
#cursor.execute('''
#    CREATE TABLE IF NOT EXISTS chat_history (
#       id INTEGER PRIMARY KEY AUTOINCREMENT,
 #       user_message TEXT,
#        assistant_response TEXT,
 #       embedding BLOB,
##        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#    )
#''')
#con.commit()
#THIS IS THE MAIN SCRIPT OF DBMS MYSQLITE3 INSERTION,DELETION AND UPDATION.

#this addition of dbms will help us to use queue,process sychronization and many more task on the users.
#control over the users


'''
Initially proposed fields for the tables are:
1. UID : unique identification for the users appear at first or even reloads it will overwriteen when user reloads the web page.
2. Domain : current domain they are downloading from eg: youtube
3. Filename: this will show the filename , which will get downloaded upon invoke.
4. download_comeplete: 1-true, 0-false, helps to checks whether an event is done to send the file back to user
5. starter: whether any event of excution or thread has been started and limits the user triggering other features
6. percentage:generally its function is not to show the percentage, 
it will hold certain values that will return into the frontend and trigger some functions,
for example,
percenatage=100-triggers the frontend to stop excuting the loading screen
7.time_of_arrival:(TOA) logs the first access time of this user
8.data: holds a json data in case of any addtional data insertion needed.

'''

import sqlite3


# Create a table
def reset_back_to_start():
    '''
    table gets reseted to original data.
    maybe copy and saved data before resetting it,? it may have use.
    '''
    # Connect to database
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()

    print("[WARNING!]You need admin privileage to clear and reset the data! Are you sure? (y/n/yes/no)")
    a = input()
    c.execute("DROP TABLE IF EXISTS users")
    if a == "y" or a == "yes":
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (uid INTEGER PRIMARY KEY AUTOINCREMENT,
                     domain TEXT  ,
                     filename TEXT  ,
                     download_complete INTEGER,
                     starter INTEGER ,
                     percentage INTEGER,
                     toa TEXT,
                     data TEXT
                     )''')


    conn.commit()

    # Close connection
    c.close()
    conn.close()


def update_this(uid, domain=None, filename=None, download_complete=None, starter=None, percentage=None, toa=None, data=None):
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    
    update_fields = []
    update_values = []
    if domain:
        update_fields.append("domain = ?")
        update_values.append(domain)
    if filename:
        update_fields.append("filename = ?")
        update_values.append(filename)
    if download_complete is not None:
        update_fields.append("download_complete = ?")
        update_values.append(download_complete)
    if starter is not None:
        update_fields.append("starter = ?")
        update_values.append(starter)
    if percentage is not None:
        update_fields.append("percentage = ?")
        update_values.append(percentage)
    if toa:
        update_fields.append("toa = ?")
        update_values.append(toa)
    if data:
        update_fields.append("data = ?")
        update_values.append(data)

    if len(update_fields) > 0:
        update_query = "UPDATE users SET " + ",".join(update_fields) + " WHERE uid = ?"
        update_values.append(uid)
        c.execute(update_query, tuple(update_values))
        conn.commit()
    conn.close()



def insert_this(domain="", filename="", download_complete=0, starter=0, percentage=0, toa="", data=None):
    '''
    values can be newely added to the db using this , any unpassed arguments results in activation
    of keyword arguments
    returns its uuid : int
    '''
    # Connect to database
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()

    if data is None:
        data = ""
    c.execute("INSERT INTO users (domain, filename, download_complete, starter, percentage, toa, data) VALUES (?, ?, ?, ?, ?, ?, ?)", (domain, filename, download_complete, starter, percentage, toa, data))
    uid = c.lastrowid
    conn.commit()

    # Close connection
    c.close()
    conn.close()

    return uid


def read_for(uid=-1):
    '''
    Reads data for certain uuids : returnType: str
    '''
    # Connect to database
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()

    if uid != -1:
        c.execute("SELECT * FROM users WHERE uid = ?", (uid,))
    else:
        c.execute("SELECT * FROM users")

    result = tuple(c.fetchone())

    # Close
    c.close()
    conn.close()

    return result

import sqlite3 

conn=sqlite3.connect("./database/SleepSchedule")
# conn=sqlite3.connect("./database/SleepSchedule") ###
cur=conn.cursor()
cur.execute("""
            CREATE TABLE user(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(25) UNIQUE NOT NULL,
                            password VARCHAR(25) NOT NULL);
            """)
cur.execute("""
            CREATE TABLE sleep(
                            sid INTEGER PRIMARY KEY AUTOINCREMENT,
                            cur_date DATE  NOT NULL,
                            start_time VARCHAR(25) NOT NULL,
                            end_time VARCHAR(25) NOT NULL,
                            duration REAL NOT NULL,
                            user_id INTEGER NOT NULL,
                            FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
                            );
            """)

def calc_diff(str1,str2):
    hr1,min1=int(str1.split(":")[0]),int(str1.split(":")[1])
    hr2,min2=int(str2.split(":")[0]),int(str2.split(":")[1])
    return abs(hr1-hr2)+abs(min1-min2)/60
# print(calc_diff("8:00","9:30"))

cur.execute("INSERT INTO user VALUES(1,'Bob','admin123');")
cur.execute("INSERT INTO sleep VALUES(1,'3/2/2024','8:00','9:30',?,1)",(calc_diff("8:00","9:30"),))
conn.commit()
conn.close()


from flask import *
import sqlite3

app=Flask(__name__)

#FIRST PAGE
@app.route("/",methods=["GET"])
def index_page():
    return render_template("index.html")

#LOGIN FORM
@app.route("/loginpage",methods=["GET"])
def login_page():
    return render_template("login.html")

#LOGIN VERIFICATION
@app.route("/login",methods=["POST"])
def login():
    uName=request.form['uName']
    uPass=request.form['uPass']
    print(uPass)
    try:
        conn=sqlite3.connect("./database/SleepSchedule")#
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("SELECT * FROM user WHERE name=? AND password=? ;",(uName,uPass))
        row=cur.fetchone()
        conn.commit()
        conn.close()
        if(row):
            return view_user(row['id'],row['name'])
        else:
            return render_template("result.html",msg="NOT VALID USER")
    except Exception as e:
        return render_template("result.html",msg=str(e))
    
#SIGNUP FORM
@app.route("/signuppage",methods=["GET"])
def signup_page():
    return render_template("signup.html")

#SIGNUP VERIFICATION
@app.route("/signup",methods=["POST"])
def signup():
    uName=request.form['uName']
    uPass=request.form['uPass']
    try:
        conn=sqlite3.connect("./database/SleepSchedule")#
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("INSERT INTO user(name,password) VALUES(?,?);",(uName,uPass))
        cur.execute("SELECT * FROM user WHERE name=? AND password=? ;",(uName,uPass))
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        for row in rows:
            break
        if(len(rows)>=1):
            return view_user(row['id'],row['name'])
        else:
            return render_template("result.html",msg="NOT VALID USER")
    except Exception as e:
        return render_template("result.html",msg=str(e))

#VIEW USER
@app.route("/viewuser",methods=["GET"])
def view_user(id,name):
    try:
        conn=sqlite3.connect("./database/SleepSchedule")#
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("SELECT * FROM user WHERE id=? AND name=? ;",(id,name))
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return render_template("user.html",rows=rows)
    except Exception as e:
        return render_template("result.html",msg=str(e))
#SLEEP PAGE
@app.route("/sleep",methods=["GET"])
def sleep_page():
    return render_template("sleepInfo.html")

#USER SLEEP FORM
@app.route("/usersleeppage",methods=["GET"])
def user_sleep_page_form():
    return render_template("usersleepForm.html")

#USER SLEEP TABLE
@app.route("/usersleep",methods=["POST"])
def get_user_sleep_page():
    uId=request.form['uId']
    try:
        conn=sqlite3.connect("./database/SleepSchedule")#
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("SELECT * FROM  sleep WHERE user_id=?;",(uId,))
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return render_template("usersleep.html",rows=rows)
    except Exception as e:
        return render_template("result.html",msg=str(e))


#ADD SLEEP PAGE
@app.route("/addsleeppage",methods=["GET"])
def add_sleep_page():
    return render_template("addsleep.html")

def calc_diff(str1,str2):
    hr1,min1=int(str1.split(":")[0]),int(str1.split(":")[1])
    hr2,min2=int(str2.split(":")[0]),int(str2.split(":")[1])
    return abs(hr1-hr2)+abs(min1-min2)/60

@app.route("/addsleep",methods=["POST"])
def add_sleep():
    uId=request.form['uId']
    cDate=request.form['cDate']
    start_time=request.form['start_time']
    end_time=request.form['end_time']
    duration=calc_diff(start_time,end_time)
    try:
        conn=sqlite3.connect("./database/SleepSchedule")#
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("INSERT INTO sleep(cur_date,start_time,end_time,duration,user_id) VALUES(?,?,?,?,?);",(cDate,start_time,end_time,duration,uId))
        conn.commit()
        conn.close()
        return render_template("result.html",msg="SUCCESSFULLY INSERTED")
    except Exception as e:
        return render_template("result.html",msg=str(e))


#ADD SLEEP PAGE
@app.route("/updatesleeppage",methods=["GET"])
def update_sleep_page():
    return render_template("updatesleep.html")

@app.route("/updatesleep",methods=["POST"])
def update_sleep():
    uId=request.form['uId']
    cDate=request.form['cDate']
    start_time=request.form['start_time']
    end_time=request.form['end_time']
    duration=calc_diff(start_time,end_time)
    try:
        conn=sqlite3.connect("./database/SleepSchedule")#
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("UPDATE sleep SET start_time=?,end_time=?,duration=? WHERE user_id=? AND cur_date=?;",(start_time,end_time,duration,uId,cDate))
        conn.commit()
        conn.close()
        return render_template("result.html",msg="SUCCESSFULLY UPDATED")
    except Exception as e:
        return render_template("result.html",msg=str(e))

#DELETE SLEEP
@app.route("/deletesleeppage",methods=["GET"])
def delete_sleep_page():
    return render_template("deletesleep.html")

@app.route("/deletesleep",methods=["POST"])
def delete_user_sleep_page():
    uId=request.form['uId']
    cDate=request.form['cDate']
    try:
        conn=sqlite3.connect("./database/SleepSchedule")#
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("DELETE FROM  sleep WHERE user_id=? AND cur_date=?;",(uId,cDate,))
        conn.commit()
        conn.close()
        return render_template("result.html",msg="SUCCESSFULLY DELETED")
    except Exception as e:
        return render_template("result.html",msg=str(e))




def main():
    app.run(debug=True)
main()
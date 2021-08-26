 

import pyrebase
import pandas as pd
config = {
    "apiKey": "AIzaSyBGbKDd5s1Nvkb6lWyQ9pX2yyEkFyjmTX8",
    "authDomain": "pmanagement-bf35b.firebaseapp.com",
    "databaseURL": "https://pmanagement-bf35b-default-rtdb.firebaseio.com",
    "projectId": "pmanagement-bf35b",
    "storageBucket": "pmanagement-bf35b.appspot.com",
    "messagingSenderId": "447964113658",
    "appId": "1:447964113658:web:2f97ebd0f5db0c604c3743",
    "measurementId": "G-LST2PN7PPT"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

from flask import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic():
	if request.method == 'POST':
		if request.form['submit'] == 'add':
                    userName = request.form['userName']
                    year = str(request.form['year'])
                    goalName = request.form['goalName']
                    goalDescription = request.form['goalDescription']
                    dateYear = str(request.form['dateYear'])
                    userRating = ""
                    managerRating = ""
                    comments = ""

                    print(userName, year, goalName, goalDescription,dateYear)
                    result = db.child("Users").child(userName).child("Goals").child(goalName).update({
                        "Description":goalDescription,
                        "Year":year,
                        "DateYear":dateYear,
                        "UserRating":userRating,
                        "ManagerRating":managerRating,
                        "Comments":comments
                    })
                    return render_template('GoalSheet.html',flag = "success")    
                    print(result)
                    
	return render_template('GoalSheet.html',flag = "failed")

@app.route('/userReview', methods=['GET', 'POST'])
def userReview() :
    user_list = db.child("Users").get().val()
    user_names = [list for list in user_list ]
    data = []
    useryear = ""
    # print(user_list)
    if request.method == "POST":
        if request.form['submit'] == 'showGoals' :
            username = request.form['userOption']
            useryear = request.form['userYear']
            print(username, useryear) 
            values = db.child("Users").child(username).child("Goals").get().val()
            val = pd.DataFrame(values)
            val = val.transpose()
            val.reset_index(inplace=True)
            print(val)
            
            for ind in val.index:
                data.append([ val['index'][ind], val['Description'][ind], val['DateYear'][ind], val['UserRating'][ind], val['Year'][ind]])
            print(data)
            return render_template('UserReview.html',userList = user_names, data = data, y = useryear, flag = "success")
            # data = val.loc["Year"]
            # print(data.tolist())
            # useryear = request.form['userYear']
        if request.form['submit'] == 'save':
            rating_val = request.form.getlist('userRat')  
            username = request.form['userOption'] 
            print(username) 
            print(rating_val, len(rating_val))
            
            if len(rating_val) == 0 :
                pass
            else:
                values = db.child("Users").child(username).child("Goals").get().val()
                val = pd.DataFrame(values)
                val = val.transpose()
                val.reset_index(inplace=True)
                print(val)
                i = 0
                for ind in val.index:
                    db.child("Users").child(username).child("Goals").child(val['index'][ind]).update({"UserRating":rating_val[i]})
                    i = i + 1
                    
                # db.child("Users").child(username).child("Goals").child('G1').update({"UserRating":rating_val[0]})

    return render_template('UserReview.html',userList = user_names, data = data, y = useryear, flag="failed")

@app.route('/managerReview', methods=['GET', 'POST'])
def managerReview() :
    user_list = db.child("Users").get().val()
    user_names = [list for list in user_list ]
    data = []
    useryear = ""
    # print(user_list)
    if request.method == "POST":
        if request.form['submit'] == 'showGoals' :
            username = request.form['userOption']
            useryear = request.form['userYear']
            print(username, useryear) 
            values = db.child("Users").child(username).child("Goals").get().val()
            val = pd.DataFrame(values)
            val = val.transpose()
            val.reset_index(inplace=True)
            print(val)
            
            for ind in val.index:
                data.append([ val['index'][ind], val['Description'][ind], val['DateYear'][ind], val['UserRating'][ind], val['ManagerRating'][ind], val['Comments'][ind], val['Year'][ind] ])
            print(data)
            # data = val.loc["Year"]
            # print(data.tolist())
            # useryear = request.form['userYear']
            return render_template('ManagerReview.html',userList = user_names, data = data, y = useryear,flag = "success")
        if request.form['submit'] == 'save':
            rating_val = request.form.getlist('managerRat')  
            manager_comm = request.form.getlist('managerComment')
            username = request.form['userOption'] 
            print(username) 
            print(rating_val, len(rating_val))
            
            if len(rating_val) == 0 :
                pass
            else:
                values = db.child("Users").child(username).child("Goals").get().val()
                val = pd.DataFrame(values)
                val = val.transpose()
                val.reset_index(inplace=True)
                print(val)
                i = 0
                for ind in val.index:
                    db.child("Users").child(username).child("Goals").child(val['index'][ind]).update({"ManagerRating":rating_val[i]})
                    db.child("Users").child(username).child("Goals").child(val['index'][ind]).update({"Comments":manager_comm[i]})
                    i = i + 1

    return render_template('ManagerReview.html',userList = user_names, data = data, y = useryear, flag="failed")

if __name__ == '__main__':
	app.run(debug=True)




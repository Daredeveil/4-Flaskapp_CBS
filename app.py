from flask import Flask,request, url_for, redirect, render_template, jsonify
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

day_dict = {'Fri':[1,0,0,0,0,0,0], 'Mon':[0,1,0,0,0,0,0],
            'Sat': [0,0,1,0,0,0,0], 'Sun':[0,0,0,1,0,0,0],
            'Thu':[0,0,0,0,1,0,0], 'Tue':[0,0,0,0,0,1,0],
            'Wed': [0,0,0,0,0,0,1]}


month_dict = {'Jan':[1,0,0,0,0,0,0,0,0,0,0,0], 'Feb':[0,1,0,0,0,0,0,0,0,0,0,0],
            'Mar': [0,0,1,0,0,0,0,0,0,0,0,0], 'Apr':[0,0,0,1,0,0,0,0,0,0,0,0],
            'May':[0,0,0,0,1,0,0,0,0,0,0,0], 'Jun':[0,0,0,0,0,1,0,0,0,0,0,0],
            'Jul':[0,0,0,0,0,0,1,0,0,0,0,0], 'Aug':[0,0,0,0,0,0,0,1,0,0,0,0],
            'Sep':[0,0,0,0,0,0,0,0,1,0,0,0], 'Oct':[0,0,0,0,0,0,0,0,0,1,0,0],
            'Nov':[0,0,0,0,0,0,0,0,0,0,1,0], 'Dec':[0,0,0,0,0,0,0,0,0,0,0,1],}

# cols = ['hour', 'is_holiday', 'day_of_week', 'month']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET'])
def predict():
    item = [x for x in request.form.values()]

    data = []

    # As the The training data was dummified one, so we have to pass the 
    # test data in the same format ('hour','is_holiday','day_of_week', 'month')
    
    data.append(int(item[0]))
    
    # is holiday
    if item[1] == 'Yes':
        data.extend([0,1])
    else:
        data.extend([1,0])
        
    # fri, mon, sat , sun, thu, tue, wed
    data.extend(day_dict[item[2]])

    # (25-08-2021) Jan, Feb, mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
    data.extend(month_dict[item[3]])
    
   
    prediction = int(model.predict([data])[0])
    

    return render_template('index.html',pred='Total Bike ride counts in the month of {} on {} at {}:00 Hrs will be {}'.format(item[3], item[2], item[0],prediction))


if __name__ == "__main__":
    app.run(debug=True)
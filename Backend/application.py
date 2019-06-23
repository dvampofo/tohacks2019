from flask import Flask, request, jsonify
import pandas as pd
import datetime

app = Flask(__name__)

def analyze(file):
    data = pd.read_csv(file)
    # Coerce date to datetime 
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Date'], axis=0, ascending=True, inplace=True)

    start_datetime = datetime.datetime(2019,5,1,0,0,0,0)
    unique_trips = 0
    for index, row in data.iterrows():
        agency = row['Transit Agency']
        type = row['Type ']
        datetime = row['Date']
        location = row['Location']

        if agency == "Toronto Transit Commission" and (type == "Transit Pass Payment" or type == "Fare Payment"):
            diff = abs(datetime - start_datetime)
            difference = diff.days * 86400 + diff.seconds
            
            if (difference > 7200): # time between trips is greater than two hours
                start_datetime = datetime
                print("----UNIQUE TRIP----")
                print("Difference", diff)
                unique_trips += 1
            
            print(datetime, location)

    print("Unique trips", unique_trips)

@app.route('/test', methods=['POST'])
def test():
    return "Sucess Azure deployment"

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        # print(file)
        # analyze(file)
        return "Success"

if __name__ == '__main__':
    app.run()
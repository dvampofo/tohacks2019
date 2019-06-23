#! usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from constants import *
import pandas as pd
import datetime

def analyse_cost(csv_file):
    data = setup_file(csv_file)

    start_datetime = datetime.datetime(2019,1,1,0,0,0,0)
    
    unique_trips = 0
    
    for index, row in data.iterrows():
        agency = row['Transit Agency']
        type = row['Type ']
        curr_datetime = row['Date']
        location = row['Location']

        if agency == TRANSIT_COMMISSION and (type == "Transit Pass Payment" or type == "Fare Payment"):
            diff = abs(curr_datetime - start_datetime)
            difference = diff.days * SEC_IN_A_DAY + diff.seconds
            
            if (difference > TWO_HOURS): # time between trips is greater than two hours
                start_datetime = curr_datetime
                print("----UNIQUE TRIP----")
                print("Difference", diff)
                unique_trips += 1
            
            print(curr_datetime, location)

    print("Unique trips", unique_trips)
    return jsonify({"Unique trips":unique_trips})


def setup_file(csv_file):
    data = pd.read_csv(csv_file)

    # Coerce date to datetime 
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Date'], axis=0, ascending=True, inplace=True)

    return data
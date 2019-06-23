#! usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from constants import *
import pandas as pd
import datetime

def analyse_cost(csv_file):
    data = setup_file(csv_file)

    start_datetime = datetime.datetime(2000,1,1,0,0,0,0)
    
    unique_trips = 0
    locations = []

    for index, row in data.iterrows():
        agency = row['Transit Agency']
        fare_type = row['Type ']
        curr_datetime = row['Date']
        location = row['Location']
        locations.append(location)

        if agency == TRANSIT_COMMISSION and (fare_type == "Transit Pass Payment" or fare_type == "Fare Payment"):
            diff = abs(curr_datetime - start_datetime)
            difference = diff.days * SEC_IN_A_DAY + diff.seconds
            
            if (difference > TWO_HOURS): # time between trips is greater than two hours
                start_datetime = curr_datetime
                """
                print("----UNIQUE TRIP----")
                print("Difference", diff)
                """
                unique_trips += 1
            
            # print(curr_datetime, location)

    unique_locations = list(set(locations))
    total_cost = round(unique_trips * TTC_ADULT_FARE, 2)
    price_difference = round(total_cost - TTC_ADULT_MONTHLY_PASS_COST, 2)

    """
    print("Unique locations", unique_locations)
    print("Unique trips", unique_trips)
    print("Total cost", total_cost)
    print("Price difference", price_difference)
    """

    return jsonify({"unique_trips":unique_trips, "total_cost":total_cost, "price_differnce":price_difference, "unique_locations":unique_locations})


def setup_file(csv_file):
    data = pd.read_csv(csv_file)

    # Coerce date to datetime 
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Date'], axis=0, ascending=True, inplace=True)

    return data
from pymongo import MongoClient
import pandas as pd
from filter_reviews_by_airline import read_from_mongodb


def search_airlines_by_aircraft(df):
    df['Aircraft'] = df.Aircraft.str.upper()
    while (command := input("About what aircraft do you want to know? Or just enter exit: ").upper().strip()) != "EXIT":
        data = []
        for i in range(len(df)):
            if df.iloc[i]['Aircraft'].__contains__(command):
                a = f"Airline: {df.iloc[i]['AirlineName']};  Country: {df.iloc[i]['OriginCountry']}\n"
                data.append(a)
        if len(data) == 0:
            print("Unfortunately, we can't find information about this aircraft.")
        else:
            for i in set(data):
                print(i)


if __name__ == "__main__":

    try:
        df = read_from_mongodb(dbname='airline_reviews', colnames='AirlineName')
        search_airlines_by_aircraft(df)

    except Exception:
        print('Unfortunately, script finished work with error.')

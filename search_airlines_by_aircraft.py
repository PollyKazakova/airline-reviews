from pymongo import MongoClient
import pandas as pd


def read_from_mongodb(dbname='airline_reviews', colnames='AirlineName'):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[dbname]
    collection = db[colnames]
    cursor = collection.find()

    data = []
    for doc in cursor:
        airline = doc['AirlineName']
        for review in doc['Reviews']:
            review['AirlineName'] = airline
            data.append(review)
    df = pd.DataFrame(data)

    return df

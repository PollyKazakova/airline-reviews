import pandas as pd
from pymongo import MongoClient
import zipfile


def read_csv_file(zip_file):
    zf = zipfile.ZipFile(zip_file)
    df = pd.read_csv(zf.open('AirlineReviews.csv'))

    return df


def delete_missing_data(df):
    df.dropna(inplace=True)

    return df


def export_to_mongodb(df, dbname='airline_reviews', colnames='AirlineNames'):
    # Подключение к MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    # Создание БД и коллекции
    db = client[dbname]
    collection = db[colnames]

    # Группировка данных по названию авиакомпании
    grouped = df.groupby('AirlineName')

    for name, group in grouped:
        airline_data = {'AirlineName': name, 'Reviews': group.drop('AirlineName', axis=1).to_dict('records')}
        collection.insert_one(airline_data)


if __name__ == "__main__":

    try:
        df = read_csv_file('AirlineReviews.zip')
        df = delete_missing_data(df)
        export_to_mongodb(df, dbname='airline_reviews', colnames='AirlineName')
        print('Your data was exported to MongoDB successfully!')

    except Exception:
        print('Unfortunately, script finished work with error. Check your zipfile and try again!')

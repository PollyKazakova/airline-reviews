from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt


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


def filter_reviews_by_airlines(df):
    df['AirlineName'] = df.AirlineName.str.upper()
    while (command := input("About what airline do you want to know? Or just enter exit: ").upper().strip()) != "EXIT":
        if command not in df['AirlineName'].unique():
            print("Sorry, we don't have information about this airline.")
        else:
            for i in df[df['AirlineName'] == command]['Review']:
                print(i, end='\n\n')
            fig = plt.figure(figsize=(6, 4))
            ax = fig.add_subplot()
            x = ['no', 'yes']
            y = [len(df[(df.AirlineName == command) & (df.Recommended == 'no')]),
                 len(df[(df.AirlineName == command) & (df.Recommended == 'yes')])]
            ax.bar(x, y, color='darkblue')
            plt.title(f'Amount of reviews with reccomendations for {command}')
            plt.show()


if __name__ == "__main__":

    try:
        df = read_from_mongodb(dbname='airline_reviews', colnames='AirlineName')
        filter_reviews_by_airlines(df)

    except Exception:
        print('Unfortunately, script finished work with error.')

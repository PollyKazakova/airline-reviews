from pymongo import MongoClient
import pandas as pd
from filter_reviews_by_airline import read_from_mongodb


def top_airlines(df):
    airlines = df['AirlineName'].unique()
    dictionary = {}
    for airline in airlines:
        dictionary[airline] = len(df[df['AirlineName'] == airline])
    df_stat = pd.DataFrame(dictionary.items(), columns=['AirlineName', 'Amount of reviews'])
    df_stat = df_stat.sort_values(by='Amount of reviews', ascending=False)
    while (command := input("If you want to watch top airlines with maximum or reviews, enter 1.\n"
                            "If you want to watch top airlines with minimum or reviews, enter 0.\n"
                            "Or just enter exit: ").title().strip()) != "Exit":
        amount = int(input("How many airlines do you want to watch? "))
        if len(df) <= amount:
            print(df)
        else:
            if command == '0':
                print(df_stat.tail(amount))
            elif command == '1':
                print(df_stat.head(amount))
            else:
                print('You entered incorrect value.')


if __name__ == "__main__":

    try:
        df = read_from_mongodb(dbname='airline_reviews', colnames='AirlineName')
        top_airlines(df)

    except Exception:
        print('Unfortunately, script finished work with error.')

import os
import requests
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import json
import csv

# output files
path = ''

f1 = open('ijambo-data.json', 'w')

f2 = open('ijambo-data.json','r')

f3 = path +'ijambo-data.csv'


BURUNDIARXIV_BASE_ID = os.getenv("BURUNDIARXIV_BASE_ID")

BURUNDIARXIV_URL = f"https://burundiarxiv-api.herokuapp.com/api/v1/{BURUNDIARXIV_BASE_ID}"


def get_data():
    """Retrieve records from BURUNDIARXIV."""
    url = BURUNDIARXIV_URL
    headers = {
      #'Authorization': f'Bearer {BURUNDIARXIV_API}',
      'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    BURUNDIARXIV_response = response.json()

    BURUNDIARXIV_records = [BURUNDIARXIV_response]

    return BURUNDIARXIV_records

def save_data():
    all_records = get_data()
    with f1:
        json.dump(all_records, f1)
    return all_records


def process_json():
    with f2:
        data = json.loads(f2.read())
        dataframe = pd.json_normalize(data, record_path =['games'])
        dataframe['list_guesses'] = [','.join(map(str, l)) for l in dataframe['guesses']]
        dataframe['count_guesses'] = dataframe['list_guesses'].str.split(',').str.len()
        #dataframe['score'] = dataframe['count_guesses'] * dataframe['time_taken']

        dataframe['converted_start_time'] = pd.to_datetime(dataframe['start_time'], utc=True)
        dataframe['start_date'] = [d.date() for d in dataframe['converted_start_time']]
        dataframe['start_hour'] = [d.time() for d in dataframe['converted_start_time']]

        dataframe['converted_end_time'] = pd.to_datetime(dataframe['end_time'], utc=True)
        dataframe['end_date'] = [d.date() for d in dataframe['converted_end_time']]
        dataframe['end_hour'] = [d.time() for d in dataframe['converted_end_time']]
        return dataframe


def dataframe_to_csv():
    data = process_json()
    data.to_csv(f3, index=None, header= True)
    return data


def main(_):
    raw_data = save_data()
    processed_data = dataframe_to_csv()

    
if __name__ == "__main__":
    main("")

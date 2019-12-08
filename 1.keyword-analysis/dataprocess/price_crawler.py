from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import os
from datetime import datetime
import re


# Config Directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'data')
KOSPI_DIR = os.path.join(DATA_DIR, 'kospi', 'price', '')
KOSDAQ_DIR = os.path.join(DATA_DIR, 'kosdaq', 'price', '')
LIST_DIR = os.path.join(os.path.dirname(CURRENT_DIR), '')
print(CURRENT_DIR)
print(DATA_DIR)
print(KOSPI_DIR)
print(KOSDAQ_DIR)
print(LIST_DIR)


def load_company_list(types):
    if types == 'kospi':
        filepath = LIST_DIR + 'kospi_list.csv'
        return pd.read_csv(filepath)
    else:
        filepath = LIST_DIR + 'kosdaq_list.csv'
        return pd.read_csv(filepath)


# Need to use "number of count" instead of "start_timestamp" and "end_timestamp"
def crawl_price_data(code_list, save_dir, timestamp_count=950):
    for code in code_list:
        print(code)

        # Base URL
        url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count={}&requestType=0"\
            .format(code, timestamp_count)

        # Load Page
        try:
            page = urllib.request.urlopen(url)
        except Exception as e:
            print(e)
            return

        # Initialize Beautiful Soup
        soup = BeautifulSoup(page, 'html.parser')

        # Extract Data From HTML
        data = []
        for item in soup.find_all('item'):
            # Extract only indices [0, 4, 5] for [period, closing, volume]
            pcv = list(np.array(item.get('data').split('|'))[[0, 4, 5]])
            pcv[0] = datetime.strptime(pcv[0], "%Y%m%d")
            data.append(pcv)
        # print(data[:5])

        # Create DataFrame
        df = pd.DataFrame(data, columns=['period', 'price', 'volume'])
        # print(df.head())

        # Save To CSV
        save_path = save_dir + "{}.csv".format(code)
        df.to_csv(save_path, index=False)


if __name__ == "__main__":
    # Load Company Lists
    kospi_list = load_company_list('kospi')
    kosdaq_list = load_company_list('kosdaq')

    # Load Code Lists
    kospi_code_list = kospi_list['종목코드'].map("{:06d}".format).values
    kosdaq_code_list = kosdaq_list['종목코드'].map("{:06d}".format).values

    # print(kospi_code_list[:5])
    # print(kosdaq_code_list[:5])

    # Crawl Price Data
    crawl_price_data(code_list=kospi_code_list, save_dir=KOSPI_DIR)
    crawl_price_data(code_list=kosdaq_code_list, save_dir=KOSDAQ_DIR)


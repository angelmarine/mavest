"""
Documentation ->
https://developers.naver.com/docs/datalab/search/#%EB%84%A4%EC%9D%B4%EB%B2%84-%ED%86%B5%ED%95%A9-%EA%B2%80%EC%83%89%EC%96%B4-%ED%8A%B8%EB%A0%8C%EB%93%9C-%EC%A1%B0%ED%9A%8C
"""

# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import pandas as pd

KEYWORD_DATA_DIR = '../data/keyword/'


def download_keyword_data(companies, company2code):
    client_id = "suYvknmMq4r40QvKrUO7"
    client_secret = "7VjhfdO2qO"
    url = "https://openapi.naver.com/v1/datalab/search"
    start_date = "2016-01-01"
    end_date = "2019-09-25"
    time_unit = "date"

    for company in companies[:2]:
        keyword_groups = [{
            "groupName": company,
            "keywords": [company]
        }]

        d = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": time_unit,
            "keywordGroups": keyword_groups
        }

        headers = {
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret': client_secret,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            url=url,
            headers=headers,
            json=d
        )
        res_code = response.status_code
        if res_code == 200:
            print("Collecting data of [{}]{}".format(company2code[company], company))
            # print(response.json()['results'][0]['data'])
            keyword_df = pd.DataFrame(data=response.json()['results'][0]['data'])

            # Save Search Data
            filepath = KEYWORD_DATA_DIR + company2code[company] + '.csv'
            if not keyword_df.empty:
                keyword_df.to_csv(filepath, index=False)
            print(keyword_df.head())
        else:
            print("Error {}: at {}".format(res_code, company))
            print(response.json())
            break


if __name__ == "__main__":
    # Load Data
    df = pd.read_csv('company_code_list.csv')

    # Preprocess
    df['종목코드'] = df['종목코드'].map("{:06d}".format)
    company2code = {row['기업명']: row['종목코드'] for idx, row in df.iterrows()}
    company_lists = df['기업명'].values

    # Download Keyword Data
    download_keyword_data(company_lists, company2code)

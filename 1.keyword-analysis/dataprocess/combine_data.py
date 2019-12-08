# Load Modules
import pandas as pd
import json
import os

# Config Directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'data')

KOSPI_PRICE_DIR = os.path.join(DATA_DIR, 'kospi', 'price', '')
KOSPI_KEYWORD_DIR = os.path.join(DATA_DIR, 'kospi', 'keyword', '')
KOSPI_COMBINED_DIR = os.path.join(DATA_DIR, 'kospi', 'combined', '')

KOSDAQ_PRICE_DIR = os.path.join(DATA_DIR, 'kosdaq', 'price', '')
KOSDAQ_KEYWORD_DIR = os.path.join(DATA_DIR, 'kosdaq', 'keyword', '')
KOSDAQ_COMBINED_DIR = os.path.join(DATA_DIR, 'kosdaq', 'combined', '')

LIST_DIR = os.path.join(os.path.dirname(CURRENT_DIR), '')

print(CURRENT_DIR)
print(DATA_DIR)
print(KOSPI_PRICE_DIR)
print(KOSDAQ_PRICE_DIR)
print(KOSPI_KEYWORD_DIR)
print(KOSDAQ_KEYWORD_DIR)
print(LIST_DIR)

# Main Functions
def load_company_list(types):
    if types == 'kospi':
        filepath = LIST_DIR + 'kospi_list.csv'
        return pd.read_csv(filepath)
    else:
        filepath = LIST_DIR + 'kosdaq_list.csv'
        return pd.read_csv(filepath)


def combine_data(company_list, price_dir, keyword_dir, save_dir):
    # Hash Maps
    code2comp = dict()
    comp2code = dict()
    for idx, row in company_list.iterrows():
        code2comp[str(row['종목코드'])] = row['기업명']
        comp2code[row['기업명']] = row['종목코드']

    # Combine Search Data and Price Data 
    # For All Companies In List
    for code in code2comp:
        print("=" * 40)
        print("Processing ", code)

        # Filepath
        price_filepath = price_dir + code + '.csv'
        keyword_filepath = keyword_dir + code + '.csv'

        # Process Price Data
        price_df = pd.read_csv(price_filepath)
        if price_df.empty:
            continue
        # price_df = price_df[['날짜', '종가', '거래량']]
        # price_df = price_df.rename(
        #     columns={'날짜': 'period', '종가': 'price', '거래량': 'volume'})  # Make column names consistent
        price_df = price_df.set_index('period')

        # Process Search Data
        try:
            keyword_df = pd.read_csv(keyword_filepath)
        except FileNotFoundError:
            continue
        if keyword_df.empty:
            continue
        keyword_df = keyword_df.set_index('period')

        # Combine
        combined_df = pd.concat([price_df, keyword_df], axis=1)
        combined_df = combined_df.dropna()
        combined_df.index.names = ['period']
        combined_df = combined_df.reset_index()
        print(combined_df.head())

        # Save
        save_path = save_dir + code + '.csv'
        combined_df.to_csv(save_path, index=False)


if __name__ == "__main__":
    # Load Company Lists
    kospi_list = load_company_list('kospi')
    kosdaq_list = load_company_list('kosdaq')
    kospi_list['종목코드'] = kospi_list['종목코드'].map("{:06d}".format)
    kosdaq_list['종목코드'] = kosdaq_list['종목코드'].map("{:06d}".format)

    # Load Code Lists
    kospi_code_list = kospi_list['종목코드'].values
    kosdaq_code_list = kosdaq_list['종목코드'].values

    # Combine Data
    combine_data(company_list=kospi_list, price_dir=KOSPI_PRICE_DIR, keyword_dir=KOSPI_KEYWORD_DIR,
                 save_dir=KOSPI_COMBINED_DIR)

    combine_data(company_list=kosdaq_list, price_dir=KOSDAQ_PRICE_DIR, keyword_dir=KOSDAQ_KEYWORD_DIR,
                 save_dir=KOSDAQ_COMBINED_DIR)

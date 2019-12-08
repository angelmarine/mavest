import pandas as pd
import urllib.request
import json


sector_codes = [
  'G10', # 에너지
  'G15', # 소재
  'G20', # 산업재
  'G25', # 경기관소비재
  'G30', # 필수소비재
  'G35', # 건강관리
  'G40', # 금융
  'G45', # IT
  'G50', # 전기통신서비스
  'G55'  # 유틸리
]

def crawl_sector_data():
    df_list = []
    for sector in sector_codes:
        url = "http://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20190220&sec_cd={}".format(sector)
        response = urllib.request.urlopen(url)
        decoded = response.read().decode('utf-8')
        data = json.loads(decoded)
        df = pd.DataFrame(data['list'])[['IDX_NM_KOR', 'CMP_CD', 'CMP_KOR']]
        df = df.rename(columns={'IDX_NM_KOR': "sector", 'CMP_CD': "code", 'CMP_KOR': "company"})
        df['sector'] = df['sector'].apply(lambda x: x.split(" ")[1])
        print(df.head())
        df_list.append(df)
    
    companies_df = pd.concat(df_list)
    companies_df.to_csv("company_sectors.csv", index=False)


if __name__ == "__main__":
    crawl_sector_data()







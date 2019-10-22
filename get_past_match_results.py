import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
import csv

URL_TEMPLATE = 'http://baseballdata.jp/{year}/{index}/GResult.html'
FILENAME_TEMPLATE = 'csv/{year}/{year}_{team}_match_results.csv'
# データ取得が可能である年度のリストを作成する
YEARS = [2014,2015,2016,2017,2018]
# サイト内のチームindexと対応するチーム名（頭文字）の辞書を作成する
DICT_TEAMS = {1:'G',2:'S',3:'DB',4:'D',5:'T',6:'C',
              7:'L',8:'F',9:'M',11:'Bs',12:'H',376:'E'}

def set_options():
    options = Options()
    # Headlessモードを有効にする
    options.set_headless(True)
    return options

def main():
    # ブラウザを起動する
    driver = webdriver.Chrome(chrome_options=set_options())

    for year in years:
        # 各年ごとに各チームの試合結果サマリーへアクセスする
        for key, value in dict_teams.items():
            # チームごとにurlを作成する
            url = (URL_TEMPLATE.format(year=year,index=key))

            # ブラウザでアクセスする
            driver.get(url)
            # 「全て見る」リンクを押下して全データを表示させる
            driver.find_element_by_class_name('allshow').click()
            sleep(1)

            # HTMLの文字コードをUTF-8に変換して取得する
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html,'html.parser')
            rows = soup.findAll('tr', class_='')

            # CSVファイルの設定
            csv_file = open(FILENAME_TEMPLATE.format(year=year,team=value),
                        'wt', newline = '', encoding = 'utf-8')
            writer = csv.writer(csv_file)

            try:
                for row in rows:
                    csv_row = []
                    for cell in row.findAll('td', bgcolor=''):
                        csv_row.append(cell.get_text().strip())
                    writer.writerow(csv_row)
            finally:
                csv_file.close()

            sleep(1)

if __name__ == "__main__":
    main()

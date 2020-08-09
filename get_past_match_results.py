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

def write_to_csv(driver, writer):
    # 「全て見る」リンクを押下して全データを表示させる
    driver.find_element_by_class_name('allshow').click()
    sleep(1)

    # HTMLの文字コードをUTF-8に変換して取得する
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html,'html.parser')
    rows = soup.findAll('tr', class_='')
    for row in rows:
        csv_row = []
        for cell in row.findAll('th', class_='pnm'):
            csv_row.append(cell.get_text().strip())
        for cell in row.findAll('td', bgcolor=''):
            csv_row.append(cell.get_text().strip())
        # 空行は無視する
        if csv_row:
            writer.writerow(csv_row)

def main():
    try:
        driver = webdriver.Chrome(chrome_options=set_options())
        driver.set_page_load_timeout(5)

        # 各年ごとに各チームの試合結果サマリーへアクセスする
        for year in YEARS:
            for index, team in DICT_TEAMS.items():
                # チームごとの試合結果掲載ページを開く
                url = (URL_TEMPLATE.format(year=year,index=index))
                driver.get(url)
                sleep(1)

                # スクレイピングした試合結果をcsvファイルに書き出す
                filename = FILENAME_TEMPLATE.format(year=year, team=team)
                with open(filename, "wt", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    write_to_csv(driver, writer)

                print("success {year} {team}".format(year=year, team=team))

    except Exception as e:
        print("error_message:{message}".format(message=e))

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
import csv

URL_TEMPLATE = 'http://baseballdata.jp/{index}/GResult.html'
FILENAME_TEMPLATE = 'csv/{year}/{year}_{team_capital}_match_results.csv'

# 現在年を取得する
this_year = datetime.date.today().year

# ブラウザのオプションを格納する変数を取得する
options = Options()
# Headlessモードを有効にする
# →コメントアウトするとブラウザが実際に立ち上がる
options.set_headless(True)
# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

# サイト内のチームindexと対応するチーム名（頭文字）の辞書を作成する
dict_teams = {1:'G',2:'S',3:'DB',4:'D',5:'T',6:'C',
              7:'L',8:'F',9:'M',11:'Bs',12:'H',376:'E'}

for key, value in dict_teams.items():
    # チームごとにurlを作成する
    url = (URL_TEMPLATE.format(index=key))

    # CSVファイルの設定
    csv_file = open(FILENAME_TEMPLATE.format(year=this_year,team_capital=value),
                    'wt', newline = '', encoding = 'utf-8')
    writer = csv.writer(csv_file)

    try:
        # ブラウザでアクセスする
        driver.get(url)
        # 「全て見る」リンクを押下して全データを表示させる
        driver.find_element_by_class_name('allshow').click()
        sleep(1)

        # HTMLの文字コードをUTF-8に変換して取得する
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html,'html.parser')

        for row in soup.findAll('tr', class_=''):
            csv_row = []
            for cell in row.findAll('td', bgcolor=''):
                csv_row.append(cell.get_text().strip())
            writer.writerow(csv_row)

        print('success team={team_capital}'.format(team_capital=value))
    except Exception as e:
        print('error_message:{message}'.format(message=e))
    finally:
        csv_file.close()

    sleep(1)

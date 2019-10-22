import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import csv

THIS_YEAR = datetime.date.today().year
START_MONTH = 3
END_MONTH = 10

URL_TEMPLATE = 'http://npb.jp/games/{year}/schedule_{month}_detail.html'
FILENAME_TEMPLATE = 'csv/{year}/{year}_schedule.csv'

# ブラウザのオプションを格納する変数を取得する
options = Options()
# Headlessモードを有効にする
# →コメントアウトするとブラウザが実際に立ち上がる
options.set_headless(True)
# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

with open(FILENAME_TEMPLATE.format(year=THIS_YEAR), 'w') as f:
    writer = csv.writer(f)
    for month in range(START_MONTH,END_MONTH + 1):
        url = URL_TEMPLATE.format(year=THIS_YEAR, month=str(month).zfill(2))
        try:
            # ブラウザでアクセスする
            driver.get(url)

            # HTMLの文字コードをUTF-8に変換して取得する
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html,'html.parser')

            for tr in soup.findAll('tr',id=re.compile('^date')):
                csv_row = []

                # 試合日を取得する
                if tr.find('th'):
                    date = tr.find('th')

                for td in tr.findAll('td'):
                    team1 = td.find('div', class_='team1')
                    team2 = td.find('div', class_='team2')
                    place = td.find('div', class_='place')
                    time = td.find('div', class_='time')

                    if team1 and team2:
                        csv_row.append(str(THIS_YEAR) + '/' + date.string[:-3])
                        csv_row.extend([team1.string, team2.string])
                    if place and time:
                        csv_row.extend([place.string, time.string])

                if csv_row and len(csv_row) == 5:
                    writer.writerow(csv_row)

            print('success target={year}/{month}'
                .format(year=THIS_YEAR, month=str(month).zfill(2)))
        except Exception as e:
            print('error_message:{message}'.format(message=e))


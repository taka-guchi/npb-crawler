import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import datetime
import csv

URL_TEMPLATE = 'http://baseballdata.jp/{index}/GResult.html'
FILENAME_TEMPLATE = 'csv/{year}/{year}_{team}_match_results.csv'
THIS_YEAR = datetime.date.today().year
# サイト内のチームindexと対応するチーム名（頭文字）の辞書
DICT_TEAMS = {1:'G',2:'S',3:'DB',4:'D',5:'T',6:'C',
              7:'L',8:'F',9:'M',11:'Bs',12:'H',376:'E'}

def set_options():
    # ブラウザのオプションを格納する変数を取得する
    options = Options()
    # Headlessモードを設定する
    options.set_headless(True)

    return options

def write_to_csv(driver, writer):
    # スクレイピング対象のtrクラス名(「全て見る」リンク押下後は空になる)
    tr_class = "deftr"
    # 「全て見る」リンクがあればクリックする
    link_all_show = driver.find_elements(By.XPATH, "//div[@class='allshow']")
    if len(link_all_show) > 0:
        driver.find_element_by_class_name("allshow").click()
        tr_class = ""
        sleep(1)

    # HTMLの文字コードをUTF-8に変換して取得
    html = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(html,'html.parser')
    for row in soup.findAll("tr", class_=tr_class):
        csv_row = []
        for cell in row.findAll("th", class_="pnm"):
            csv_row.append(cell.get_text().strip())
        for cell in row.findAll("td", bgcolor=""):
            csv_row.append(cell.get_text().strip())
        # 空行は無視する
        if csv_row:
            writer.writerow(csv_row)

def main():
    try:
        driver = webdriver.Chrome(chrome_options=set_options())
        driver.set_page_load_timeout(5)

        for index, team in DICT_TEAMS.items():
            filename = FILENAME_TEMPLATE.format(year=THIS_YEAR, team=team)
            with open(filename, "wt", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # チームごとの試合結果掲載ページを開く
                url = URL_TEMPLATE.format(index=index)
                driver.get(url)
                sleep(1)
                # スクレイピング => 試合結果をcsvファイルに書き出す
                write_to_csv(driver, writer)

            print("success team={team}".format(team=team))

    except Exception as e:
        print("error_message:{message}".format(message=e))

if __name__ == "__main__":
    main()

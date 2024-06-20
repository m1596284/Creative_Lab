# -*- coding: utf-8 -*-
# 2023_0914 v5 loading module

# Load standard library
import sys
from pathlib import Path
import time
import datetime
import threading

# Load third-party library
import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
import pygsheets
import pandas as pd

# Load local library
from test_tool.py_logging import py_logger, close_log, remove_old_log
from test_tool.sqlite_CRUD import Database

# set path and name
py_path = Path(__file__).parent
py_name = Path(__file__).stem
project_path = Path(__file__).parent.parent
project_name = Path(__file__).parent.stem
log_path = f"{project_path}/log"
log_name = f"{project_name}_{py_name}"
logger_name = f"{project_name}_{py_name}"
config_path = f"{project_path}/config"

# set logger
# remove_old_log(log_path=log_path, log_name=py_name)
log = py_logger("w","INFO",log_path,log_name,__name__)

# load line notify token
with open(f"{config_path}/test_token.json", encoding="utf-8") as f:
    tokens_json = json.load(f)
    test_token = tokens_json["test_lab"]["token"]

# main function
def main():
    log.info(f"function: {sys._getframe().f_code.co_name}")
    while True:
        crawl_page()
        time.sleep(60*10)
    msg = "test end"
    line_notify(test_token, msg)


def crawl_page(thread_number=1):
    log.info(f"function: {sys._getframe().f_code.co_name}, thread_number = {thread_number}")
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control':'max-age=0',
        'Sec-Ch-Ua':'"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"macOS"',
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    main_url = "https://www.g2a.com/search?query=netflix%20turkey&sort=price-highest-first"
    r = requests.get(main_url, headers=headers, timeout=10)
    r_text = r.content.decode("utf-8")
    r_text = r.text
    soup = BeautifulSoup(r_text, "html.parser")
    price_list = soup.find_all('span', class_='sc-iqAclL sc-crzoAE dJFpVb eqnGHx sc-bqGGPW gjCrxq')
    point_list = soup.find_all('h3', class_='sc-iqAclL sc-dIsUp dJFpVb eHDAgC sc-daBunf brOVbM')
    if len(price_list) == len(point_list):
        point_price_dict = {}
        for index, point in enumerate(point_list):
            if "Netflix Key" in point.get_text().strip():
                point = point.get_text().strip().replace("Netflix Gift Card ","").replace(" - Netflix Key - TURKEY","")
                point = point[:point.find(" ")]
                price = price_list[index].get_text().strip().replace("$ ","")
                point_price_dict[point] = str(round(float(point)/float(price),1))
                log.info(point)
                log.info(price)
                log.info(round(float(point)/float(price),1))
        gc = pygsheets.authorize(service_account_file=f'{config_path}/gsheet_secrets.json')
        gsheet_url = "https://docs.google.com/spreadsheets/d/1buoEcY0K5qdSpiRnCzi9pmXAtvXz6g_Fd0z02m8VrVw/edit?hl=zh-tw#gid=0"
        sh = gc.open_by_url(gsheet_url)
        ws = sh.worksheet_by_title(f"price_sheet")
        point_list = ws.get_col(1, include_tailing_empty=False)
        rate_list = []
        temp_point_list = []
        temp_rate_list = []
        for point in point_list:
            if point in point_price_dict:
                rate_list.append(point_price_dict[point])
            else:
                if point == "point":
                    rate_list.append(datetime.datetime.now().strftime("%m%d_%H:%M"))
        for new_point in point_price_dict:
            if new_point not in point_list:
                temp_point_list.append(new_point)
                temp_rate_list.append(point_price_dict[new_point])
        point_list += temp_point_list
        rate_list += temp_rate_list
        point_list_df = pd.DataFrame(point_list)
        rate_list_df = pd.DataFrame(rate_list)
        ws.insert_cols(col=1, number=1, inherit=False)
        ws.set_dataframe(point_list_df, 'A1', copy_index=False, copy_head=False)
        ws.set_dataframe(rate_list_df, 'B1', copy_index=False, copy_head=False)

def multi_threads(job, thread_quantity=2):
    log.info(f"function: {sys._getframe().f_code.co_name}, thread_quantity = {thread_quantity}")
    thread_list = []
    # thread start
    for thread_number in range(thread_quantity):
        thread_list.append(threading.Thread(target=job, args=[thread_number]))
        thread_list[thread_number].start()
    # wait all thread finish
    for thread_number in range(thread_quantity):
        thread_list[thread_number].join()


def line_notify(token, msg):
    log.info(f"function: {sys._getframe().f_code.co_name}, msg = {msg}")
    token = test_token
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {"message": msg}
    notify_status = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=params, timeout=10
    )
    log.debug(f"notify_status: {notify_status}")

if __name__ == "__main__":
    # set Database
    db_name = py_name
    db_path = f"{project_path}/database/{db_name}.sqlite3"
    db = Database(db_path=db_path)
    table = "test_table"
    table_dict = {
        "video_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "video_url": "TEXT",
        "video_number": "TEXT",
        "video_name": "TEXT",
        "video_date": "TEXT",
        "video_tags": "TEXT",
    }
    db.create_table(table, table_dict)
    db.use_table(table)
    # db.delete_all()

    # start main
    main()

    # close database
    db.close()

    # close log
    close_log(log)

# -*- coding: utf-8 -*-
# 2023_1102 v1 init

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

# load line notify token
with open(f"{config_path}/test_token.json", encoding="utf-8") as f:
    tokens_json = json.load(f)
    test_token = tokens_json["test_lab"]["token"]


def main():
    log.info(f"function: {sys._getframe().f_code.co_name} start")
    msg = "test start"
    line_notify(test_token, msg)
    crawl_page()
    # multi_threads(job, thread_quantity)
    # multi_threads(crawl_page, 3)
    msg = "test end"
    line_notify(test_token, msg)


def crawl_page(thread_number=1):
    log.info(f"function: {sys._getframe().f_code.co_name}, thread_number = {thread_number}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }
    main_url = "https://www.bosch-home.com.tw/product-list/dishwashers/freestanding-dishwashers/freestanding-dishwashers-with-60cm-width"
    r = requests.get(main_url, headers=headers, timeout=10)
    r_text = r.content.decode("utf-8")
    r_text = r.text
    product_list_string = r_text[r_text.find('{"response":'):r_text.find("</script>",r_text.find('{"response":'))]
    product_list_dict = json.loads(product_list_string)
    # for key in product_list_dict.keys():
    #     log.info(key)

    for item in product_list_dict["response"]["items"]:
        item_info_string = ""
        item_info_dict = {
        "sku" : item["headers"][5],
        "series" : item["headers"][0],
        "machine_type" : item["headers"][1],
        "size" : item["headers"][3],
        "color" : item["headers"][4],
        "price" : item["price"]["value"],
        "link" : item["link"],
        }
        for key in item_info_dict.keys():
            item_info_string += f"{item_info_dict[key]},"
        log.info(item_info_string)

    # div_list = soup.find_all("div", {"class": ["class1", "class2"]})
    # div_tag = soup.find_all("div", class_="class1")
    # span_list = soup.find_all("span", attrs={"name": "CarrierCode"})
    # tree = etree.HTML(r_text)
    # tree_result = tree.xpath("")


def multi_threads(job, thread_quantity=2):
    log.info(f"function: {sys._getframe().f_code.co_name}, thread_quantity = {thread_quantity}")
    threads = []
    # thread start
    for thread_number in range(thread_quantity):
        threads.append(threading.Thread(target=job, args=[thread_number]))
        threads[thread_number].start()
    # wait all thread finish
    for thread_number in range(thread_quantity):
        threads[thread_number].join()


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
    # set logger
    # remove_old_log(log_path=log_path, log_name=py_name)
    log = py_logger(
        "w",
        level="DEBUG",
        log_path=log_path,
        log_name=log_name,
        logger_name=logger_name,
    )
    log.info(f"__main__ start, py_name = {py_name}")
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

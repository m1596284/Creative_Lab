# -*- coding: utf-8 -*-
# 2022_0810 v1
import time
import datetime
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from py_logging import py_logger, close_log, remove_old_log
from sqlite_CRUD import Database
from lxml import etree


def main():
    log.info(f"***** Test start *****")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    main_url = f"https://www.ixxx.com/a-z/?pricing=free#mobile-anchor-top"
    r = requests.get(main_url, headers=headers)
    # r_text = r.content.decode("utf-8")
    r_text = r.text
    soup = BeautifulSoup(r_text, 'html.parser')
    # log.info(soup.prettify())
    # all_div_muli_class = soup.find_all('div',{'class':['class1','class2']})
    all_div_single_class = soup.find_all('li', class_="category")
    for thing in all_div_single_class:
        log.info(f"{thing.a.get_text().replace(thing.a.span.get_text(),'')}_____{thing.a.span.get_text()}")
    # tree = etree.HTML(r_text)
    # tree_result = tree.xpath("")


def line_notify(token, msg):
    msg = f'\nstart'
    token = "ppe8qq75KOiH87Rv1Zn6oYqXI0EfU7odbGLIHXUUCaj"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    return requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)


if __name__ == "__main__":
    # set path and name
    here_dir = Path(__file__).parent
    py_name = Path(__file__).stem

    # set logger
    remove_old_log(log_path=f"{here_dir}/log", file_name=py_name)
    log = py_logger("w", level="INFO", log_path=f"{here_dir}/log", file_name=py_name)

    # set Database
    db_name = py_name
    db_path = f"{here_dir}/{db_name}.sqlite3"
    db = Database(db_path=f"{db_path}")
    table = "test_table"
    table_dict = {
        "id": "integer",
        "name": "text",
        "url": "text",
    }
    db.create_table(table, table_dict)
    db.use_table(table)
    # db.delete_all()

    # start test
    main()

    # close database
    db.close()

    # close log
    close_log(log)

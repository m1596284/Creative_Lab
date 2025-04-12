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

# Load local library
from py_logging import py_logger, close_log, remove_old_log
from sqlite_CRUD import Database

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
log = py_logger("w", "INFO", log_path, log_name, logger_name)


# load line notify token
with open(f"{config_path}/test_token.json", encoding="utf-8") as f:
    tokens_json = json.load(f)
    test_token = tokens_json["test_lab"]["token"]


# main function
def main():
    log.info(f"function: {sys._getframe().f_code.co_name}")
    msg = "test start"
    line_notify(test_token, msg)
    crawl_page()
    # multi_threads(job=crawl_page, thread_quantity=3)
    msg = "test end"
    line_notify(test_token, msg)


def crawl_page(thread_number=1):
    log.info(f"function: {sys._getframe().f_code.co_name}, thread_number = {thread_number}")
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Cookie': 'locale=zh-TW; _hjSessionUser_1979059=eyJpZCI6IjdmMWE0ODgwLWNiNzQtNTlhNS04NmRhLTMyYjUyZDMxOGNlOCIsImNyZWF0ZWQiOjE3MDkxOTAwNzM5MTUsImV4aXN0aW5nIjp0cnVlfQ==; user_display_name_v2=m1596284; user_avatar_url_v2=https%3A%2F%2Fwww.gravatar.com%2Favatar%2Fe67f37ca432bb13de552fc8348917932.png; user_id_v2=12096; user_time_zone_v2=Asia%2FTaipei; user_time_zone_offset_v2=28800; kktix_session_token_v2=dbb40a89cc8fc1ff6c2edd586b6bfc17; user_path_v2=%2F; mobileNotVerified=0; _gid=GA1.2.1899437218.1709691295; _clck=ofjg98%7C2%7Cfju%7C0%7C1520; _hjSession_1979059=eyJpZCI6IjhlOTA0MjA0LTU1MzktNDIyYS04MjU2LWRlYjhkYjJjZmE0YSIsImMiOjE3MDk2OTkzMjU0MDksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; XSRF-TOKEN=VRd1Fg%2FcvaYZG4rOmDz8upwSLZBRlpYhN7YDhfHfnsUCjEQers7Dybq1EFK9blhwPr1iKeUjT0LQMNUaKIrZBw%3D%3D; _ga_LWVPBSFGF6=GS1.1.1709699325.7.1.1709704214.60.0.0; _clsk=1ia6uan%7C1709704214328%7C305%7C1%7Cd.clarity.ms%2Fcollect; _ga_SYRTJY65JB=GS1.1.1709699325.7.1.1709704214.60.0.0; _ga=GA1.2.1578728527.1709190074; _ga_WZBYP4N1ZG=GS1.2.1709699325.7.1.1709704214.60.0.0',
        'Referer': 'https://kktix.com/events/w8a2gthy02/registrations/new',
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    main_url = "https://kktix.com/events/w8a2gthy02/registrations/new"
    response = requests.get(main_url, headers=headers, timeout=10)
    response_text = response.content.decode("utf-8")
    response_text = response.text
    log.info((response_text.count("已售完")))
    soup = BeautifulSoup(response_text, "html.parser")
    log.info(soup.prettify())
    # div_list = soup.find_all("div", {"class": ["class1", "class2"]})
    # div_tag = soup.find_all("div", class_="class1")
    # span_list = soup.find_all("span", attrs={"name": "CarrierCode"})
    # tree = etree.HTML(r_text)
    # tree_result = tree.xpath("")


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
    notify_status = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params, timeout=10)
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

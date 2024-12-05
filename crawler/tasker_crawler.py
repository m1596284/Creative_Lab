# -*- coding: utf-8 -*-
# 2023_0914 v5 loading module

# Load standard library
import sys
from pathlib import Path
import time

# Load third-party library
import requests
import json

# Load local library
from test_area.py_logging import py_logger, close_log
from test_area.sqlite_CRUD import Database

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
log = py_logger("w", "INFO", log_path, log_name, __name__)

# load line notify token
with open(f"{config_path}/line_notify_token.json", encoding="utf-8") as f:
    tokens_json = json.load(f)
    takser_token = tokens_json["takser"]["token"]


# main function
def main():
    log.info(f"function: {sys._getframe().f_code.co_name}")
    search_keys = [
        "python",
        "程式",
        "軟體",
        "資料",
        "網站",
        "網頁",
        "爬蟲",
        "爬取",
        "抓取",
        "數據",
        "API",
    ]
    for search_key in search_keys:
        crawl_page(search_key)
        time.sleep(5)
    # line_notify(takser_token, "Tasker Crawler Done")


def crawl_page(search_key):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    log.info(f"search_key: {search_key} page: 1")
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Basic',
        'content-length': '70',
        'content-type': 'application/json',
        'cookie': '_gcl_au=1.1.1268845188.1726740368; _fbp=fb.2.1726740367755.405428248743238306; PHPSESSID=caf71789a51fb618f00b44fdc97778907d30043e; _ga=GA1.1.1603255885.1713937450; _tt_enable_cookie=1; _ttp=fY6a8BnR8ukj1c4c9TSoFIuH_YO.tt.2; bearerToken=eyJpdiI6ImVLbEVtVXl6QkdOZGpMRlg2c2FIdFE9PSIsInZhbHVlIjoiZkJrQVhNaXYzS3hDc0FwY2N2TWlWdldFQis1dWl2aEVOaE9vNCtWYUtPTnhkVndjcFhucmZ4VGNkZE02bHFsMVdER1lHWmxQSUVVRFFvc3ZEb1RiUVA0NHBqR3N3OVFZYkxNRlhlbXJsaEpCbnBQczVLZE1vRGRGVU1kcmUwWkkzWmJDXC9mVHBiaUFnbTdLNXRYZDJoZz09IiwibWFjIjoiM2U0OTRhOGQxMjhlZjM0ZDA3MTU5OGM3MTViNDdmZDhhZDZlNjg3Y2M4YzBkYjFiNjYzMjJjMzViZjJlM2M0YSJ9; sidebarMain=profile; _umil=-%2C3505486%2C; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22lWPtB8wkMm2XR4cvu2Sn%22%2C%22expiryDate%22%3A%222025-11-29T09%3A03%3A42.903Z%22%7D; _uetsid=d136b470ae3011efb85bc53352c7bb07; _uetvid=ac33985001fd11ef91cf712528200bca; _ga_ZSLGL1E8E5=GS1.1.1732871016.3.1.1732871024.52.0.1874139508; _ga_N38MLP384G=GS1.1.1732871016.4.1.1732871025.51.0.1239732493; XSRF-TOKEN=eyJpdiI6IllBNGFZS0JFMzg0OHM4VzZWRjJQRHc9PSIsInZhbHVlIjoiNmJ0RVhQZCtLajBMM1NCZmpoZTVnZVlIaU15V2NYQ0RHRHNWRUdIRGZaSEkwdUlkdyttbEI1ejJ2OTg3ODQ0VmNcL2hpYm5KQW5PTXl5SXF5ZjVIbHZ4bWFqYTZuZlNZdjhvenhcL3JUNGhxMUZLMGZ3SjJSeXFuYUJ5TXJiUk5yOCIsIm1hYyI6IjdlNDcxZGUxYjM1MmNhOGFmNGNhMDU4MTNhYWIzNzU3MzE2M2VlYmIxMjM1MmZiN2FlMmFkZmMzZGExNGZjNDgifQ%3D%3D',
        'origin': 'https://www.tasker.com.tw',
        'priority': 'u=1, i',
        'referer': 'https://www.tasker.com.tw/case/list',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-xsrf-token': 'eyJpdiI6IllBNGFZS0JFMzg0OHM4VzZWRjJQRHc9PSIsInZhbHVlIjoiNmJ0RVhQZCtLajBMM1NCZmpoZTVnZVlIaU15V2NYQ0RHRHNWRUdIRGZaSEkwdUlkdyttbEI1ejJ2OTg3ODQ0VmNcL2hpYm5KQW5PTXl5SXF5ZjVIbHZ4bWFqYTZuZlNZdjhvenhcL3JUNGhxMUZLMGZ3SjJSeXFuYUJ5TXJiUk5yOCIsIm1hYyI6IjdlNDcxZGUxYjM1MmNhOGFmNGNhMDU4MTNhYWIzNzU3MzE2M2VlYmIxMjM1MmZiN2FlMmFkZmMzZGExNGZjNDgifQ==',
    }
    request_api = "https://www.tasker.com.tw/api/v2/case/list/data"
    payload = {"lo": [], "ca": "", "page": 1, "st": 1, "sc": [], "mo": [], "se": search_key, "so": 1, "a_id": "", "gclid": ""}
    response = requests.post(request_api, json=payload, headers=headers, timeout=10)
    response_json = response.json()
    # log.info(f"response_json: {response_json}")
    task_id_records = db.read_column("task_id")
    task_id_records_list = []
    for task in task_id_records:
        task_id_records_list.append(task[0])
    # total_page = response_json["total_page"]
    task_list = response_json["list"]
    log.info(f"task_list: {task_list}")
    check_record(task_list, task_id_records_list)  # check first page
    # for page in range(2, total_page+1): # check other pages
    #     log.info(f"search_key: {search_key} page: {page}")
    #     payload["page"] = page
    #     response = requests.post(request_api, json=payload, headers=headers, timeout=10)
    #     response_json = response.json()
    #     task_id_records = db.read_column("task_id")
    #     task_id_records_list = []
    #     for task in task_id_records:
    #         task_id_records_list.append(task[0])
    #     total_page = response_json["total_page"]
    #     task_list = response_json["list"]
    #     check_record(task_list, task_id_records_list)
    #     time.sleep(5)


def check_record(task_list, task_id_records_list):
    for task in task_list:
        # task_id = task["case_id"]
        task_id = task["tk_no"]
        task_update_time = task["time_text"]
        task_title = task["case_name"]
        task_pay = task["money"]
        task_place = task["address"]
        task_due_date = task["deadline"]
        task_description = task["content"]
        task_url = f"https://www.tasker.com.tw/case/detail/{task_id}"
        if task_id in task_id_records_list:
            pass
        elif task_update_time == "今天":
            db.create(
                task_id=task_id,
                task_title=task_title,
                task_pay=task_pay,
                task_place=task_place,
                task_due_date=task_due_date,
                task_description=task_description,
                task_url=task_url,
            )
            line_notify(takser_token, f"\n{task_title}\n{task_pay}\n{task_place}\n{task_due_date}\n{task_description}\n{task_url}")


def line_notify(token, msg):
    log.info(f"function: {sys._getframe().f_code.co_name}")
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
    table = "task_list"
    table_dict = {
        "task_number": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "task_id": "TEXT",
        "task_title": "TEXT",
        "task_pay": "TEXT",
        "task_place": "TEXT",
        "task_due_date": "TEXT",
        "task_description": "TEXT",
        "task_url": "TEXT",
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

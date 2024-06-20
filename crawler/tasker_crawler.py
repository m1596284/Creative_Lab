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
with open(f"{config_path}/line_notify_token.json", encoding="utf-8") as f:
    tokens_json = json.load(f)
    takser_token = tokens_json["takser"]["token"]

# main function
def main():
    log.info(f"function: {sys._getframe().f_code.co_name}")
    search_keys = ["python",
                   "程式",
                   "軟體",
                   "資料",
                   "網站",
                   "網頁",
                   "爬蟲",
                   "爬取",
                   "數據",
                   ]
    for search_key in search_keys:
        crawl_page(search_key)
        time.sleep(5)
    line_notify(takser_token, "Tasker Crawler Done")


def crawl_page(search_key):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    log.info(f"search_key: {search_key} page: 1")
    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization':'Basic',
        'Content-Length':'91',
        'Content-Type':'application/json',
        'Cookie':'agent_id_19374_click=eyJpdiI6ImlEd3NObTVjT2RMXC9HMlNHWTVpdnVnPT0iLCJ2YWx1ZSI6ImVxejc5TVNIb0xEdjFZcEl1RjV6T21jQTN6cmRkY2ljSDhRSjltbEd3YUVXS3hRc3Y2Z2U4cTJ4NFloMVJRdDUiLCJtYWMiOiI0YTA4M2ZhMjRlZTVmNjAxY2M2ZjAwMzk3MWE1NzBhOThiMmZkZmMyMGM2OGI3NjFmNjg4OWJjMThiYzYwMTdjIn0%3D; _gcl_aw=GCL.1712811779.CjwKCAjw8diwBhAbEiwA7i_sJQKyH_qFRTYEpoM1h8M4Dp63qb_L9BcHdQVnlNmt6TiXleo2_ZT1XRoCcJkQAvD_BwE; _gcl_au=1.1.631976425.1712811779; _gac_UA-138445576-1=1.1712811797.CjwKCAjw8diwBhAbEiwA7i_sJQKyH_qFRTYEpoM1h8M4Dp63qb_L9BcHdQVnlNmt6TiXleo2_ZT1XRoCcJkQAvD_BwE; sidebarMain=profile; _umil=-%2C3505486%2C; _gid=GA1.3.404954407.1713178963; login_token=eyJpdiI6IjUyVzRZalorWXJEZ1BKT1NkSVhIekE9PSIsInZhbHVlIjoieWZ3ZDJveGRuRjgwRVoyK0FXNUhDemtnQXBMQWlNc3FNbWFjUDB2Sm9NT3ZjZ05tb2ppYUsyUjd5VXV0a3J5YTRmempyZ3VaUEFmZVZ1XC91QVM2WTlrbm15TnNOd21pVUE2XC82XC8rK3NSQVl2UWpIQWpEWENYaFJJMUNOTmJJQVV0Z3JRV0E4YlpGMVFOQStnVmVZdmM2THphWXQydk5hV2pKc09RSjF3OEY0OTM0VG5TUFZ3VFZXb05EM1RGRTFDYTAwQ0JSY3F5OW9vaU9Ga3AyVTE1U3B0eWRVRGlTWVh4QW4rVVp0Zm16ejl0MWg2YU9seko2Q3NXZXlYWlwvdUl3M0licmE1ZUpaZ1VUbVFuenB5SVJFY0ZHdVcwSlZnam5qWFNHUG1FaE9MQXNHXC9ZU3BjY2JBSVBtY0d4SlNmV3dkR3NPU0d2YzB6QUQwc1VuaGYzUFVtd2oyS2JmKzEwKzY0c2tFZ3FkbkVTdjYxVGxLRzQ5SnhYa0h5d0hpMzFJenA4NXVJMnRZQnNkb0JiaTZkbm84WEhGNGU3S3B2dVJxS1BqT0NOQVBrPSIsIm1hYyI6ImJlNzA2OWI2YjgxNmUzZGMwM2UwMDY1MjlmZDc5NTljOGYwYTAyOGJjYjgwODM0ZGVhZDA5NzgxYjk2ZjEwMzMifQ%3D%3D; up=eyJpdiI6IkVcL0JDbTlzVkZMRVNYQTNZb084XC9BUT09IiwidmFsdWUiOiJ1MVdXVW1iZXRMQ3RadW9McHhVV2hQVUFaWFVpOTU0cERQUWdiUTU1S2ZhaERkVTQ5WjRoNG9hbTQyaWVDMStqIiwibWFjIjoiZWI1YjVmOTExZDI5NWI3ZTU5OTg4MjViYjYyYjZkY2M5OGRhMGM1ZjQ0M2FhZGZjOTc1MzY2NjkxMzE5ODI4NyJ9; upd=eyJpdiI6IjMwSjF3Y1Zhc01GMUJYYUZRbW1vMFE9PSIsInZhbHVlIjoiYlJMUUw3ajFGRVZtWDhIeFRlcnI3a1VPRnk0QURNOXRYNEl3ZllJVUdxbm0rdURLeWtUejRyQUZubmZcL2dORHkiLCJtYWMiOiJjMjIxMzc4MDhkMmM1OWE5NDU2ZTZkNWEwMTJjODIzYTU2M2E2M2E0MzM1ZjZiMjI1ZjY0YTIxYTEyZjdkYzY3In0%3D; uc=eyJpdiI6IktLaDhLZE1WaklhYVA4WjF4NVA3TGc9PSIsInZhbHVlIjoiUDFHQ0lxZVZxMmxzRTdkclAzc2d4Y0JcL3FPdThNODJTU2NxKzVpbVBKM0tzQTBNZkpvVEFqTEoydVd1SGpaUGIiLCJtYWMiOiIzNzE5ZjQ3NjI1M2IyNjJlMjI1N2Q2OWY5MzM4OWRmNmNjOGE4OGUxMmU3OTI0ZjI1NThhY2UzNTQ0ZDM4OTU3In0%3D; ucd=eyJpdiI6ImFqd0p3a3hoeVJocVhBVUYwYTNtVXc9PSIsInZhbHVlIjoiSjdISnJhVTZoQ3R1M1hsaHBBSnpQR3JOTzRYVzd1ODNNV0hmS0VyRHJ0MjhVNGVSZ1IreWIrNDV6WklpSGtqWSIsIm1hYyI6IjEwOTI1MTU5OGM3MTdlZTljZmUyNzEwMDMxMzY2ODMzNTZhZGQ2ZmZmMTZlMWQ2MWQ3ZjQ5MDc2ZjcxMzZjZDEifQ%3D%3D; agent_id_19358_click=eyJpdiI6Imd4NEZOXC9KVnVGWVM4dmFLVjJJMUV3PT0iLCJ2YWx1ZSI6IjYraDNFVVNWS2lFTllGZmk2YWpwQ1wvbEl0eGt3XC9oWERadllPNjk5ekdTcFVmMnhLSHFvTTRGcys0d1VqTVg2SSIsIm1hYyI6ImY4ZmZiODJmMmZiMzlmM2E0YjA4Y2Q5ZDQ1NzQxMjJjM2RlMjcxZjhiNzVhOTE1YTRmNGI2Y2YwYWJhM2ZmMTUifQ%3D%3D; PHPSESSID=e86e3b30bccc814dda3e2b2be475f1e67c9d2f21; ut=eyJpdiI6IkgzNVdDS1ozUDdRbFhBcmR6QmhtWlE9PSIsInZhbHVlIjoidGxUbUNTNFRnd0FJTGxKbVZJaFNDdFlVRzNJVGxIXC9QY3NvT25vb0VVNWFmaGh5VXN2THp0eFkxZFhtb2ZcLzhOIiwibWFjIjoiOWJkNTYzY2Y2YzBjYjcxODcyOWJlM2IyZGI5ODBkOGQyNzFhY2IyZTY1ZTU5M2Q1NTNjNTVmNzU0ZGRiODk1MyJ9; house_questionnaire=1; _gat_UA-138445576-1=1; _ga=GA1.1.299147133.1712811779; _ga_N38MLP384G=GS1.1.1713274829.10.1.1713276685.50.0.1623963088; _uetsid=aeb9fb60fb1711eeb15acd5950732957; _uetvid=70666460d5df11ed99114b50cebde2c9; XSRF-TOKEN=eyJpdiI6IlNuWnBOT0c0SGJTeU1mZHdvTVVNMGc9PSIsInZhbHVlIjoidURrUkVXejh6OXdQTXFkV2lxaTM2MTBiUnFreE5TYnJhRzZYZmVGdlY3K3FPVlJVdE8wenJqc1VEbjNTSU91REtPcEpMMVZKTFJOZGx6ZjZlSDJ2TlZucDgyR1VtdVlQNHJYRmhWMlJRQWx2NUxpalhkMXQ4UDV0K2F6YWRGNVQiLCJtYWMiOiJlYmI1MjBkMzU1YTA3NzBhZmY3NmNjNjQ4YWQ4OGQzZDFjYjdiNGZjODBiYTRiOWI4OWI4YWZlMWQyOTgwMzYxIn0%3D',
        'Origin':'https://www.tasker.com.tw',
        'Referer':'https://www.tasker.com.tw/case/list?se=python&page=2',
        'Sec-Ch-Ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"macOS"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Xsrf-Token':'eyJpdiI6IlNuWnBOT0c0SGJTeU1mZHdvTVVNMGc9PSIsInZhbHVlIjoidURrUkVXejh6OXdQTXFkV2lxaTM2MTBiUnFreE5TYnJhRzZYZmVGdlY3K3FPVlJVdE8wenJqc1VEbjNTSU91REtPcEpMMVZKTFJOZGx6ZjZlSDJ2TlZucDgyR1VtdVlQNHJYRmhWMlJRQWx2NUxpalhkMXQ4UDV0K2F6YWRGNVQiLCJtYWMiOiJlYmI1MjBkMzU1YTA3NzBhZmY3NmNjNjQ4YWQ4OGQzZDFjYjdiNGZjODBiYTRiOWI4OWI4YWZlMWQyOTgwMzYxIn0=',
    }
    request_api = "https://www.tasker.com.tw/api/v2/case/list/data"
    payload = {
        "lo": [],
        "ca": "",
        "page": 1,
        "st": 1,
        "sc": [],
        "mo": [],
        "se": search_key,
        "so": 1,
        "a_id": "",
        "gclid": ""
    }
    response = requests.post(request_api, json=payload, headers=headers, timeout=10)
    response_json = response.json()
    task_id_records = db.read_column("task_id")
    task_id_records_list = []
    for task in task_id_records:
        task_id_records_list.append(task[0])
    # total_page = response_json["total_page"]
    task_list = response_json["list"]
    check_record(task_list, task_id_records_list) # check first page
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
        task_id = task["case_id"]
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
    notify_status = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=params, timeout=10
    )
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

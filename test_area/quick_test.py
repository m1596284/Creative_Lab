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
with open(f"{config_path}/test_token.json", encoding="utf-8") as f:
    tokens_json = json.load(f)
    test_token = tokens_json["test_lab"]["token"]
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie':'ASP.NET_SessionId=0ucgmp0xsoom5h0wqgh5aqab; _gid=GA1.2.1058861182.1717562060; _ga_L558FCL13P=GS1.1.1717720840.9.1.1717720847.0.0.0; sg=ip=114.34.22.219&sessionid=1324035&loginsys=sg; _ga=GA1.2.389225597.1714534613; _gat_nauiTracker=1; _gat=1; _ga_7X4B3Y4GEW=GS1.2.1717726686.4.1.1717730436.0.0.0; _ga_0P823DCZSG=GS1.2.1717726686.4.1.1717730436.0.0.0; sgx=771139237',
        'Priority':'u=0, i',
        'Referer':'https://elearning.naui.org/course/~d2zqhh0un00C0t1t1s124rz1Waq2442r11oA228c10960762r0012u1f22gh7oyI0',
        'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"macOS"',
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

# main function
def main():
    log.info(f"function: {sys._getframe().f_code.co_name}")
    start_key = 19065
    start_value = 1
    perious_score = 0
    start_answer_dict = {
        "a19063": "1",
        "a19064": "3",
        "a19065": "2",
        "a19066": "2",
        "a19067": "2",
        "a19068": "3",
        "a19069": "2",
        "a19070": "1",
        "a19071": "1",
        "a19072": "1",
        "a19073": "1",
        "a19074": "1",
        "a19075": "1",
        "a19076": "1",
        "a19077": "1",
        "a19078": "1",
        "a19079": "1",
        "a19080": "1",
        "a19081": "1",
        "a19082": "1",
        "a19083": "1",
        "a19084": "1",
        "a19085": "1",
        "a19086": "1",
        "a19087": "1",
        "a19088": "1",
        "a19089": "1",
        "a19090": "1",
        "a19091": "1",
        "a19092": "1",
        "a19093": "1",
        "a19094": "1",
        "a19095": "1",
        "a19096": "1",
        "a19097": "1",
        "a19098": "1",
        "a19099": "1",
        "a19100": "1",
        "a19101": "1",
        "a19102": "1",
        "a19103": "1",
        "a19104": "1",
        "a19105": "1",
        "a19106": "1",
        "a19107": "1",
        "a19108": "1",
        "a19109": "1",
        "a19110": "1",
        "a19111": "1",
        "a19112": "1",
        "a19113": "1",
        "a19114": "1",
        "a19115": "1",
        "a19116": "1",
        "a19117": "1",
        "a19118": "1",
        "a19119": "1",
        "a19120": "1",
        "a19121": "1",
        "a19122": "1",
        "a19123": "1",
        "a19124": "1",
        "a19125": "1",
        "a19126": "1",
        "a19127": "1",
        "a19128": "1",
        "a19129": "1",
        "a19130": "1",
        "a19131": "1",
        "a19132": "1",
        "a19133": "1",
        "a19134": "1",
        "a19135": "1",
        "a19136": "1",
        "a19137": "1",
        "a19138": "1",
        "a19139": "1",
        "a19140": "1",
        "a19141": "1",
        "a19142": "1",
        "a19143": "1",
        "a19144": "1",
        "a19145": "1",
        "a19146": "1",
        "a19147": "1",
        "a19148": "1",
        "a19149": "1",
        "a19150": "1",
        "a19151": "1",
        "a19152": "1",
        "a19153": "1",
        "a19154": "1",
        "a19155": "1",
        "a19156": "1",
        "a19157": "1",
        "a19158": "1",
        "a19159": "1",
        "a19160": "1",
        "a19161": "1",
        "a19162": "1",
    }
    start_exam_page = "c00a101nTSqr1K5r7l17P89T0Br00T09g4g780K0H08P8g940i0101nr2B50Ukp"
    result_page, used_answer_dict = take_exam(start_exam_page,start_answer_dict)
    new_score, next_exam_page = read_result(result_page)
    log.info(f"new_score = {new_score}")
    log.info(f"next_exam_page = {next_exam_page}")
    # while True:
    #     try:
    #         result_page, used_answer_dict = take_exam(start_exam_page,start_answer_dict)
    #         new_score, next_exam_page = read_result(result_page)
    #         log.info(f"new_score = {new_score}")
    #         log.info(f"next_exam_page = {next_exam_page}")
    #         while new_score != 10:
    #             try:
    #                 time.sleep(2)
    #                 log.info(f"next_exam_page = {next_exam_page}")
    #                 result_page, used_answer_dict = take_exam(next_exam_page,used_answer_dict)
    #                 log.info(f"result_page = {result_page}")
    #                 log.info(f"used_answer_dict = {used_answer_dict}")
    #                 new_score, next_exam_page = read_result(result_page)
    #                 log.info(f"new_score = {new_score}")
    #                 log.info(f"next_exam_page = {next_exam_page}")
    #                 if new_score < perious_score:
    #                     start_value -= 1
    #                 elif new_score == perious_score :
    #                     start_value += 1
    #                 elif new_score > perious_score:
    #                     start_key += 1
    #                 perious_score = new_score
    #                 used_answer_dict = {
    #                     f"a{start_key}": f"{start_value}",
    #                 }
    #                 log.info(used_answer_dict)
    #                 log.info(f"key = a{start_key}, value = {start_value}")
    #             except:
    #                 log.info("error")
    #                 time.sleep(2)
    #     except:
    #         log.info("start error")
    #         time.sleep(2)
    # test()

def take_exam(exam_page,input_answer_dict):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    main_url = f"https://elearning.naui.org/course/~{exam_page}?startexam"
    response = requests.get(main_url, headers=headers, timeout=10)
    response_text = response.text
    soup = BeautifulSoup(response_text, "html.parser")
    # log.info(soup.prettify())
    examid = soup.find("input", id="examid").get("value")
    pageid = soup.find("input", id="pageid").get("value")
    exampageid = soup.find("input", id="exampageid").get("value")
    formValidation = soup.find("input", id="formValidation").get("value")
    # log.info(f"examid = {examid}")
    # log.info(f"pageid = {pageid}")
    # log.info(f"exampageid = {exampageid}")
    # log.info(f"formValidation = {formValidation}")
    form_data = {
        "a": "gradeexam",
        "examid": examid,
        "pageid": pageid,
        "exampageid": exampageid,
        "formValidation": formValidation,
    }
    form_data.update(input_answer_dict)
    main_url = "https://elearning.naui.org/course/events.aspx"
    response = requests.get(main_url, headers=headers, data=form_data, timeout=10)
    result_page = response.text
    # log.info(response_text)
    return result_page,input_answer_dict

def read_result(result_page):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    main_url = f"https://elearning.naui.org/course/{result_page}"
    response = requests.get(main_url, headers=headers, timeout=10)
    response_text = response.text
    soup = BeautifulSoup(response_text, "html.parser")
    # log.info(soup.prettify())
    score = int(soup.find("h5", {"class": "grade"}).get_text()[2:4])
    next_exam_page = soup.find("a", {"class": "stdButton"}).get("href")
    next_exam_page = next_exam_page[1:]
    next_exam_page = next_exam_page[:next_exam_page.find("?")]
    return score,next_exam_page

def test():
    next_exam_page = "!eo1x11Z108v60Ro5H82H0l05YI220Nf46v9NXyo11y0Yv011YBd604p4a1Q2SN9?startexam"
    next_exam_page = next_exam_page[1:]
    log.info(f"next_exam_page = {next_exam_page}")
    next_exam_page = next_exam_page[:next_exam_page.find("?")]
    log.info(f"next_exam_page = {next_exam_page}")

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
    # start main
    main()

    # close log
    close_log(log)

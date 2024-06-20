# -*- coding: utf-8 -*-
import time
import datetime
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from py_logging import py_logger, close_log, remove_old_log
from sqlite_CRUD import Database
import sys
import threading
import csv
import sqlite3
import unicodedata

# set path and name
py_path = Path(__file__).parent
py_name = Path(__file__).stem
project_name = Path(__file__).parent.stem
log_path = f"{py_path}/log"
log_name = project_name
logger_name = f"{project_name}_{py_name}"
config_path = f"{py_path}/config"


# set logger
log = py_logger("a", level="INFO", log_path=log_path, log_name=log_name, logger_name=logger_name)
with open(f"{config_path}/test_token.json", encoding="utf-8") as f:
    tokens_json = json.load(f)
    test_token = tokens_json["test_lab"]["token"]


def main():
    log.info(f"{sys._getframe().f_code.co_name}: Test start")
    # crawl all url from each page
    # page_number_list = [i for i in range(1, 1644)]
    # multi_threads(crawl_url, 2, page_number_list)

    # crawl all info from each url
    # video_url_list = []
    # url_list = db.read_all("video_url")
    # for each_url in url_list:
    #     if each_url[3] == "":
    #         video_url_list.append(each_url[2])
    # log.info(f"rest {len(video_url_list)}")
    # multi_threads(crawl_info, 2, video_url_list)

    # crawl my saved url
    # crawl_my_saved()

    # analysis tags
    analysis_tag()

    pass


def crawl_url(page_number_list, thread_number=1):
    log.info(f"{sys._getframe().f_code.co_name}")
    db = Database(db_path=db_path)
    table = "test_table"
    db.use_table(table)
    while len(page_number_list) > 0:
        page_number = page_number_list.pop()
        # log.info(f"{page_number_list} {page_number}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        }
        main_url = f"https://missav.com/ja/fc2?page={page_number}"
        r = requests.get(main_url, headers=headers, timeout=10)
        r_text = r.text
        soup = BeautifulSoup(r_text, "html.parser")
        all_div_single_class = soup.find_all("a", class_="text-secondary")
        for page_link in all_div_single_class:
            log.info(f"{thread_number}: {page_link['href']}")
            video_info = {
                "video_url": page_link["href"],
                "video_number": "",
                "video_name": "",
                "video_date": "",
                "video_tags": "",
                "last_modified_date": datetime.datetime.now(),
            }
            db.create(video_info)
    db.close()


def crawl_info(video_url_list, thread_number=1):
    log.info(f"{sys._getframe().f_code.co_name}")
    db = Database(db_path=db_path)
    table = "test_table"
    db.use_table(table)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }
    # main_url = "https://missav.com/ja/fc2-ppv-3667893"
    # main_url = "https://missav.com/ja/fc2-ppv-3650883"
    while len(video_url_list) > 0:
        main_url = video_url_list.pop()
        log.info(f"{thread_number} {len(video_url_list)} {main_url}")
        r = requests.get(main_url, headers=headers, timeout=10)
        r_text = r.text
        soup = BeautifulSoup(r_text, "html.parser")
        video_name = soup.find("h1", class_="text-base").text.replace("'", "''")
        # log.info(video_name)
        div_single_class = soup.find("div", class_="space-y-2")
        all_div_single_class = div_single_class.find_all("div", class_="text-secondary")
        # log.info(len(all_div_single_class))
        video_date = all_div_single_class[0].find("span", class_="font-medium").text
        # log.info(video_date)
        video_number = all_div_single_class[1].find("span", class_="font-medium").text
        # log.info(video_number)
        video_tags = ""
        if len(all_div_single_class) == 3:
            all_video_tags = all_div_single_class[2].find_all("a")
            for a_tag in all_video_tags:
                # log.info(a_tag.text)
                video_tags += f"{a_tag.text},"
        video_info_dict = {
            "video_url": main_url,
            "video_number": video_number,
            "video_name": video_name,
            "video_date": video_date,
            "video_tags": video_tags,
            "last_modified_date": datetime.datetime.now(),
        }
        db.update(video_info_dict, f"video_url = '{video_info_dict['video_url']}'")
    db.close()


def crawl_my_saved(thread_number=1):
    log.info(f"{sys._getframe().f_code.co_name}")
    video_url_list = []
    for page_number in range(1, 41):
        main_url = f"https://missav.com/ja/saved?page={page_number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Cookie": 'user_uuid=3849cf96-4fb1-4918-8a3f-68f32226152e; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InZxclJxeEpUTTNvWXE0UWYrKzB1b3c9PSIsInZhbHVlIjoiL3IwOGsxQzVsdmxvVlNxTFJ1djQ0MHVmYnVXVG5oQlJ1Yk1OcmhFV1VpejNVQStEUlN5OS8xRWtMdFZaRmMyaC9NOUswNDVaY1BLNUlRTWswMVZBUno5Q2t6TWFvTVBTcnI5WDNURzcvZWhtNWlHNXM1eTN5REZ3NEtac0NTQ0tTeDR1Z1k5alBoNFpadDVscmJrL2VFeWdYTDVWU1VubE1QZStFamZOSllIWU4yUXZJUEN0cFRGdlFXN1p2RGJzSS9IaUgrTVU2c080aHFqRzZoTS9sNVNabU9WYXpHUzBUOUdmdTMyd3BhTT0iLCJtYWMiOiI5NTJhMmYwMGVkZDcwNzkyNTY4MzcxNjFjNDljMzc2ZDBjYmIzNjdjOTAxYmFiMTEzMzA0ODY5YzdkZGQyMjRiIiwidGFnIjoiIn0%3D; bnState={"impressions":24,"delayStarted":0}; _ga_Z3V6T9VBM6=deleted; sb_onpage_62bdca270715b3b43fbac98597c038f1=0; _gid=GA1.2.677237759.1692020303; search_history=[%22%25EF%25BC%2593%25E5%25A4%25A7%25E7%25A5%259E%22%2C%22%25E5%25A4%25A7%25E7%25A5%259E%22%2C%22%25E8%25A8%2593%25E7%25B7%25B4%22%2C%223132230%22%2C%22%25E5%25A4%25A7%25E5%25A5%25B6%22]; localized=1; cf_clearance=VnBVulp.daX0V1QIrk_9q6WpJbyaxTcZ8DWTtxsAcEM-1692333091-0-1-3881a54f.fd5512af.e63ccae2-0.2.1692333091; XSRF-TOKEN=eyJpdiI6IitpOTdxTnI3TVNxN2pCSnNGKzI4WUE9PSIsInZhbHVlIjoiTGZ0Tk0ycEdWU2I1eGFvTHh2b2FQcUJpejU4VmFYR2VqYmcvM0dRTmJQRWdOWElBcmdxeklQYStNVnhUR1JVNVV5K3JoQkdvMFJQRGphdkl0WkRKc0tOREVZUjFUY1BMTm9ZV1BWcXREeUQrbzlyNWdycXBOQTBkbk5nN1BiRTYiLCJtYWMiOiI4ZTEwY2ZlZTEwOGFkNjY2ODUyYzk2M2NkZTc0ZmM0ZDNiNTM1MTFlOTU0YmFlZjI3Zjc0ZmFlYzYzMTUwN2Q4IiwidGFnIjoiIn0%3D; missav_session=eyJpdiI6Ik1ndUM5eWNwREFra0d1dWZRbldnZVE9PSIsInZhbHVlIjoiWGJ5V3U3SElZbmFpSVhkK1VpZ1hpS3dJemJ3QjQwT3BOZ0JjUUVob2tOanJaTHJTdlVaNzJodGNtalBWVE1wY1lNUmN0NXpIMXFvTzh2TnlqYWRqZ0xTSXJuSDB2VE1RblZXeHBScTFsNm5qR0ZLOHUyeWhpdENlU3BMY3RTY3kiLCJtYWMiOiJlYWY3ZTE0MzZjM2NlYjIzZmU2NTZmMjNkMDc0M2FiNTIyOGRmNzI5ZmIyMTJkYjdhMDJlZThlODYwMDc4OGUwIiwidGFnIjoiIn0%3D; ciHGadjqpAyj27iRdTT6S05P6fatBx51NGE1dmKm=eyJpdiI6InRqa0hET2swL1E4bzhOSHN0cXoxN3c9PSIsInZhbHVlIjoicGtGR2t3S2pXTzBOc1d4T0VwZm9FdnZ0RmpyS2FNS2NGRkRkcm0zYTNZaWh6U2x2eUNoYmlla2pTb21rMGZqQkVDeXdHNVdoakhNaEZMRUlXeDk0Ym9QYzYvVVRneUZIQXl0WHJ6bnZkWjdGQlFXQUsxRDcrY05kV01PcVlwS1RrQ2NsY2lzbDBESDV2Wms0aGpheWpMM1IxRTRQTkxJQU9TOTJ3UHdNT0psWWNxRnRteS8zNDVrcnRyR3lsRDY3TGZDV1l0dW1xRUZsbWcybXUwWXRDQlZtenVhWkJ0NWJVdE5CTUxCMFBKdEM5bEVlSzMxU0ZUeWNYbEp6Vk9OQXgrYTcvanhnZDVFS2R2ZGtidDBWSHRxajZ0ZEhhVHgvUHpqZ0V0aSs5LzV6UXR5N2ZzbU50UmpFcEdJWHBzWldYY1lJVjg3cGVoVUNNQVI1VWhtZU55cDR6a1NIbjVEKzlIS3l0SzNTMjN2UTlaVkNKcmtPbE5KM2pHZGdUYmNNUEJNL0tWSmUwMllJZ0FVWVU0R1pMbGZKaXZsY1pPUXQvNnFVSFYzdDQzSXdQMDdHVkxkaDRpWlNyU3NsaWtDMi9sczRsSHFRenh0ZVo0NzdhclRpODhLT3Q0NlM3M2ZKVTZLeHBYRUYzN042MmxPaVRMUjA5NkxEaFlNMUlWUVE5TFJad1FBSHhqc1F4cWtDYnJmZ0JvQWUrYnhXZGx2WVE2cDRsUWRsTTFtRWwyTHJ4YTBHTkppTzdpZVRuZTBCSFZYaWw3VmJ6WHhrUFhlV0FqNjgrdz09IiwibWFjIjoiMGJlMWUyYzUzZjAyNjlhZTg3MDg2YzY3ZjY3MWEwMTkzZTYzNzgwM2YwNzM4NGEzYTZiMTg0ZDQ0Yjk4NzE1MSIsInRhZyI6IiJ9; _gat_UA-177787578-14=1; _ga_Z3V6T9VBM6=GS1.1.1692333091.95.1.1692333151.0.0.0; _ga=GA1.1.1076591210.1674616221',
        }
        # log.info(f"{thread_number} {len(video_url_list)} {main_url}")
        r = requests.get(main_url, headers=headers, timeout=10)
        r_text = r.text
        soup = BeautifulSoup(r_text, "html.parser")
        a_tag = soup.find_all("a", class_="text-secondary")
        for each_a_tag in a_tag:
            log.info(each_a_tag["href"])
            video_url_list.append(each_a_tag["href"])
        # log.info(len(a_tag))
    log.info(video_url_list)


def analysis_tag(thread_number=1):
    log.info(f"{sys._getframe().f_code.co_name}: thread {thread_number}")
    # count all tags
    video_tags_list = db.read_column("video_tags")
    video_tag_count_dict = {}
    video_tag_split_list = []
    for video_tags in video_tags_list:
        video_tags = str(video_tags[0])
        video_tags = video_tags.replace("\u3000", ",")
        video_tags = video_tags.replace("\n", ",").replace("、", ",")
        video_tags = convert_to_halfwidth(video_tags)
        each_tag_list = video_tags.split(",")
        video_tag_split_list.append(each_tag_list)
        for each_tag in each_tag_list:
            if video_tag_count_dict.get(each_tag):
                video_tag_count_dict[each_tag] += 1
            else:
                video_tag_count_dict[each_tag] = 1
    # video_tag_count_dict = dict(sorted(video_tags_dict.items(), key=lambda item: item[1]))
    # log.info(video_tag_count_dict)

    # calculate weight of each tag
    value_sum = 0
    video_tags_weigth_dict = {}
    for key, value in video_tag_count_dict.items():
        if key != "":
            value_sum += value
    for key, value in video_tag_count_dict.items():
        tag_weight = round(value / value_sum * 100, 3)
        # log.info(f"{key}{tag_weight}")
        video_tags_weigth_dict[key] = tag_weight
    # log.info(video_tags_weigth_dict)

    # calculate origin score
    for each_tag_list in video_tag_split_list:
        origin_score = 0
        for each_tag in each_tag_list:
            if each_tag != "":
                origin_score += video_tags_weigth_dict[each_tag]
        origin_score = round(origin_score, 3)
        # log.info(f"{origin_score}")

    # count my saved tags
    video_url_list = [
        "https://missav.com/ja/fc2-ppv-3083109",
        "https://missav.com/ja/fc2-ppv-3081943",
        "https://missav.com/ja/fc2-ppv-3072842",
        "https://missav.com/ja/fc2-ppv-1167350",
        "https://missav.com/ja/fc2-ppv-3076115",
        "https://missav.com/ja/fc2-ppv-3072037",
        "https://missav.com/ja/fc2-ppv-3070096",
        "https://missav.com/ja/fc2-ppv-3067890",
        "https://missav.com/ja/fc2-ppv-3060957",
        "https://missav.com/ja/fc2-ppv-3117174",
        "https://missav.com/ja/fc2-ppv-3053921",
        "https://missav.com/ja/fc2-ppv-3049163",
        "https://missav.com/ja/fc2-ppv-3092584",
        "https://missav.com/ja/fc2-ppv-3009616",
        "https://missav.com/ja/fc2-ppv-3006756",
        "https://missav.com/ja/fc2-ppv-3006673",
        "https://missav.com/ja/fc2-ppv-3029118",
        "https://missav.com/ja/fc2-ppv-3132230",
        "https://missav.com/ja/fc2-ppv-2511710",
        "https://missav.com/ja/fc2-ppv-1119396",
        "https://missav.com/ja/fc2-ppv-3581881",
        "https://missav.com/ja/fc2-ppv-2954735",
        "https://missav.com/ja/fc2-ppv-2953018",
        "https://missav.com/ja/fc2-ppv-2949026",
        "https://missav.com/ja/fc2-ppv-2950054",
        "https://missav.com/ja/fc2-ppv-2950069",
        "https://missav.com/ja/fc2-ppv-2949996",
        "https://missav.com/ja/fc2-ppv-2943344",
        "https://missav.com/ja/fc2-ppv-2942945",
        "https://missav.com/ja/fc2-ppv-3200292",
        "https://missav.com/ja/fc2-ppv-2923773",
        "https://missav.com/ja/fc2-ppv-2938137",
        "https://missav.com/ja/fc2-ppv-2919003",
        "https://missav.com/ja/fc2-ppv-2921066",
        "https://missav.com/ja/fc2-ppv-2859042",
        "https://missav.com/ja/fc2-ppv-2855312",
        "https://missav.com/ja/fc2-ppv-2856504",
        "https://missav.com/ja/fc2-ppv-2843783",
        "https://missav.com/ja/fc2-ppv-2805736",
        "https://missav.com/ja/fc2-ppv-2807589",
        "https://missav.com/ja/fc2-ppv-2806053",
        "https://missav.com/ja/fc2-ppv-2781074",
        "https://missav.com/ja/fc2-ppv-2767654",
        "https://missav.com/ja/fc2-ppv-2767568",
        "https://missav.com/ja/fc2-ppv-2763672",
        "https://missav.com/ja/fc2-ppv-2790333",
        "https://missav.com/ja/fc2-ppv-2760777",
        "https://missav.com/ja/fc2-ppv-2751830",
        "https://missav.com/ja/fc2-ppv-2749053",
        "https://missav.com/ja/fc2-ppv-2747209",
        "https://missav.com/ja/fc2-ppv-2744995",
        "https://missav.com/ja/fc2-ppv-2745772",
        "https://missav.com/ja/fc2-ppv-2737605",
        "https://missav.com/ja/fc2-ppv-2735957",
        "https://missav.com/ja/fc2-ppv-2731896",
        "https://missav.com/ja/fc2-ppv-2731996",
        "https://missav.com/ja/fc2-ppv-3078940",
        "https://missav.com/ja/fc2-ppv-2730022",
        "https://missav.com/ja/fc2-ppv-2724757",
        "https://missav.com/ja/fc2-ppv-2735981",
        "https://missav.com/ja/cus-1811",
        "https://missav.com/ja/fc2-ppv-3104502",
        "https://missav.com/ja/fc2-ppv-2663992",
        "https://missav.com/ja/fc2-ppv-3482842",
        "https://missav.com/ja/fc2-ppv-3430890",
        "https://missav.com/ja/fc2-ppv-3377076",
        "https://missav.com/ja/fc2-ppv-3259992",
        "https://missav.com/ja/fc2-ppv-3090722",
        "https://missav.com/ja/fc2-ppv-2644948",
        "https://missav.com/ja/fc2-ppv-2639188",
        "https://missav.com/ja/fc2-ppv-2632743",
        "https://missav.com/ja/fc2-ppv-2629651",
        "https://missav.com/ja/fc2-ppv-2624792",
        "https://missav.com/ja/fc2-ppv-2619318",
        "https://missav.com/ja/fc2-ppv-2623769",
        "https://missav.com/ja/fc2-ppv-2615407",
        "https://missav.com/ja/fc2-ppv-2610406",
        "https://missav.com/ja/fc2-ppv-2606034",
        "https://missav.com/ja/fc2-ppv-2607893",
        "https://missav.com/ja/fc2-ppv-2603072",
        "https://missav.com/ja/fc2-ppv-2578614",
        "https://missav.com/ja/fc2-ppv-2577989",
        "https://missav.com/ja/fc2-ppv-2582507",
        "https://missav.com/ja/fc2-ppv-2577307",
        "https://missav.com/ja/fc2-ppv-2571039",
        "https://missav.com/ja/fc2-ppv-2571330",
        "https://missav.com/ja/fc2-ppv-2560104",
        "https://missav.com/ja/fc2-ppv-2559379",
        "https://missav.com/ja/fc2-ppv-2550183",
        "https://missav.com/ja/fc2-ppv-2552123",
        "https://missav.com/ja/fc2-ppv-2549115",
        "https://missav.com/ja/fc2-ppv-2534088",
        "https://missav.com/ja/fc2-ppv-2536231",
        "https://missav.com/ja/fc2-ppv-2526023",
        "https://missav.com/ja/fc2-ppv-2526771",
        "https://missav.com/ja/fc2-ppv-2523207",
        "https://missav.com/ja/fc2-ppv-2519228",
        "https://missav.com/ja/fc2-ppv-238629",
        "https://missav.com/ja/fc2-ppv-2498047",
        "https://missav.com/ja/fc2-ppv-2496909",
        "https://missav.com/ja/fc2-ppv-2486345",
        "https://missav.com/ja/fc2-ppv-2484996",
        "https://missav.com/ja/fc2-ppv-2466403",
        "https://missav.com/ja/fc2-ppv-2896877",
        "https://missav.com/ja/fc2-ppv-2504509",
        "https://missav.com/ja/ppz-016-uncensored-leak",
        "https://missav.com/ja/fc2-ppv-1683292",
        "https://missav.com/ja/fc2-ppv-2463393",
        "https://missav.com/ja/fc2-ppv-2449641",
        "https://missav.com/ja/fc2-ppv-795111",
        "https://missav.com/ja/fc2-ppv-2444682",
        "https://missav.com/ja/fc2-ppv-2442741",
        "https://missav.com/ja/fc2-ppv-2444266",
        "https://missav.com/ja/fc2-ppv-2553638",
        "https://missav.com/ja/fc2-ppv-2427261",
        "https://missav.com/ja/fc2-ppv-2401268",
        "https://missav.com/ja/fc2-ppv-2380636",
        "https://missav.com/ja/fc2-ppv-2368983",
        "https://missav.com/ja/fc2-ppv-2369256",
        "https://missav.com/ja/fc2-ppv-1919130",
        "https://missav.com/ja/fc2-ppv-2368488",
        "https://missav.com/ja/fc2-ppv-2363548",
        "https://missav.com/ja/fc2-ppv-2364487",
        "https://missav.com/ja/fc2-ppv-2373835",
        "https://missav.com/ja/fc2-ppv-3107617",
        "https://missav.com/ja/fc2-ppv-3404291",
        "https://missav.com/ja/fc2-ppv-2237812",
        "https://missav.com/ja/fc2-ppv-2224163",
        "https://missav.com/ja/fc2-ppv-2213597",
        "https://missav.com/ja/fc2-ppv-2204960",
        "https://missav.com/ja/fc2-ppv-2183631",
        "https://missav.com/ja/fc2-ppv-1973430",
        "https://missav.com/ja/fc2-ppv-2066579",
        "https://missav.com/ja/fc2-ppv-2060033",
        "https://missav.com/ja/fc2-ppv-2042116",
        "https://missav.com/ja/fc2-ppv-2098827",
        "https://missav.com/ja/fc2-ppv-1952605",
        "https://missav.com/ja/fc2-ppv-1949449",
        "https://missav.com/ja/fc2-ppv-1937050",
        "https://missav.com/ja/fc2-ppv-1932561",
        "https://missav.com/ja/fc2-ppv-1928548",
        "https://missav.com/ja/fc2-ppv-2421170",
        "https://missav.com/ja/fc2-ppv-1882790",
        "https://missav.com/ja/fc2-ppv-1892883",
        "https://missav.com/ja/fc2-ppv-1926164",
        "https://missav.com/ja/fc2-ppv-1920886",
        "https://missav.com/ja/fc2-ppv-1922324",
        "https://missav.com/ja/fc2-ppv-1917351",
        "https://missav.com/ja/fc2-ppv-1912446",
        "https://missav.com/ja/fc2-ppv-1787250",
        "https://missav.com/ja/fc2-ppv-1913271",
        "https://missav.com/ja/fc2-ppv-1912328",
        "https://missav.com/ja/fc2-ppv-1884714",
        "https://missav.com/ja/fc2-ppv-1874667",
        "https://missav.com/ja/fc2-ppv-1867550",
        "https://missav.com/ja/fc2-ppv-1865212",
        "https://missav.com/ja/fc2-ppv-1863908",
        "https://missav.com/ja/fc2-ppv-1861191",
        "https://missav.com/ja/fc2-ppv-1852669",
        "https://missav.com/ja/fc2-ppv-1852875",
        "https://missav.com/ja/fc2-ppv-1839722",
        "https://missav.com/ja/fc2-ppv-1822965",
        "https://missav.com/ja/fc2-ppv-1818320",
        "https://missav.com/ja/fc2-ppv-1818390",
        "https://missav.com/ja/fc2-ppv-2481982",
        "https://missav.com/ja/fc2-ppv-1827920",
        "https://missav.com/ja/fc2-ppv-3100741",
        "https://missav.com/ja/fc2-ppv-1791544",
        "https://missav.com/ja/fc2-ppv-1787200",
        "https://missav.com/ja/fc2-ppv-1765188",
        "https://missav.com/ja/fc2-ppv-1782713",
        "https://missav.com/ja/fc2-ppv-1773451",
        "https://missav.com/ja/fc2-ppv-1764861",
        "https://missav.com/ja/fc2-ppv-1763171",
        "https://missav.com/ja/fc2-ppv-1759707",
        "https://missav.com/ja/fc2-ppv-1805559",
        "https://missav.com/ja/fc2-ppv-1758667",
        "https://missav.com/ja/fc2-ppv-1031688",
        "https://missav.com/ja/fc2-ppv-1755831",
        "https://missav.com/ja/fc2-ppv-1734672",
        "https://missav.com/ja/fc2-ppv-1733195",
        "https://missav.com/ja/fc2-ppv-1731698",
        "https://missav.com/ja/fc2-ppv-2639886",
        "https://missav.com/ja/fc2-ppv-2906385",
        "https://missav.com/ja/fc2-ppv-1726550",
        "https://missav.com/ja/fc2-ppv-1722149",
        "https://missav.com/ja/fc2-ppv-1702264",
        "https://missav.com/ja/fc2-ppv-1696503",
        "https://missav.com/ja/fc2-ppv-1676368",
        "https://missav.com/ja/fc2-ppv-1672101",
        "https://missav.com/ja/fc2-ppv-1663634",
        "https://missav.com/ja/fc2-ppv-1664296",
        "https://missav.com/ja/fc2-ppv-1658366",
        "https://missav.com/ja/fc2-ppv-1641843",
        "https://missav.com/ja/fc2-ppv-1655430",
        "https://missav.com/ja/fc2-ppv-1662496",
        "https://missav.com/ja/fc2-ppv-1645418",
        "https://missav.com/ja/fc2-ppv-1636780",
        "https://missav.com/ja/fc2-ppv-1627713",
        "https://missav.com/ja/fc2-ppv-1624838",
        "https://missav.com/ja/fc2-ppv-1612619",
        "https://missav.com/ja/fc2-ppv-1616189",
        "https://missav.com/ja/fc2-ppv-1611460",
        "https://missav.com/ja/fc2-ppv-3280265",
        "https://missav.com/ja/fc2-ppv-3174490",
        "https://missav.com/ja/fc2-ppv-1587448",
        "https://missav.com/ja/fc2-ppv-1601853",
        "https://missav.com/ja/fc2-ppv-1602136",
        "https://missav.com/ja/fc2-ppv-1599295",
        "https://missav.com/ja/fc2-ppv-1593539",
        "https://missav.com/ja/fc2-ppv-1567328",
        "https://missav.com/ja/fc2-ppv-1566327",
        "https://missav.com/ja/fc2-ppv-1560667",
        "https://missav.com/ja/fc2-ppv-1557572",
        "https://missav.com/ja/fc2-ppv-1554066",
        "https://missav.com/ja/fc2-ppv-1552869",
        "https://missav.com/ja/fc2-ppv-1541587",
        "https://missav.com/ja/fc2-ppv-1532811",
        "https://missav.com/ja/fc2-ppv-1531006",
        "https://missav.com/ja/fc2-ppv-1509932",
        "https://missav.com/ja/fc2-ppv-1514223",
        "https://missav.com/ja/fc2-ppv-1508574",
        "https://missav.com/ja/fc2-ppv-1500329",
        "https://missav.com/ja/fc2-ppv-1519442",
        "https://missav.com/ja/fc2-ppv-1516255",
        "https://missav.com/ja/fc2-ppv-1518963",
        "https://missav.com/ja/fc2-ppv-1510788",
        "https://missav.com/ja/fc2-ppv-1514178",
        "https://missav.com/ja/fc2-ppv-1516399",
        "https://missav.com/ja/fc2-ppv-1490794",
        "https://missav.com/ja/fc2-ppv-1488237",
        "https://missav.com/ja/fc2-ppv-1443546",
        "https://missav.com/ja/fc2-ppv-1476959",
        "https://missav.com/ja/fc2-ppv-1490802",
        "https://missav.com/ja/fc2-ppv-1488540",
        "https://missav.com/ja/fc2-ppv-1484744",
        "https://missav.com/ja/fc2-ppv-1477837",
        "https://missav.com/ja/fc2-ppv-1473962",
        "https://missav.com/ja/fc2-ppv-1483851",
        "https://missav.com/ja/fc2-ppv-1481986",
        "https://missav.com/ja/fc2-ppv-1482778",
        "https://missav.com/ja/fc2-ppv-1479839",
        "https://missav.com/ja/fc2-ppv-1475093",
        "https://missav.com/ja/fc2-ppv-1406445",
        "https://missav.com/ja/fc2-ppv-1419847",
        "https://missav.com/ja/fc2-ppv-1417107",
        "https://missav.com/ja/fc2-ppv-1417547",
        "https://missav.com/ja/fc2-ppv-1416711",
        "https://missav.com/ja/fc2-ppv-1415477",
        "https://missav.com/ja/fc2-ppv-1409293",
        "https://missav.com/ja/fc2-ppv-1407033",
        "https://missav.com/ja/fc2-ppv-3067877",
        "https://missav.com/ja/fc2-ppv-1911550",
        "https://missav.com/ja/fc2-ppv-1962384",
        "https://missav.com/ja/fc2-ppv-1399049",
        "https://missav.com/ja/fc2-ppv-1394523",
        "https://missav.com/ja/fc2-ppv-1394913",
        "https://missav.com/ja/fc2-ppv-1392723",
        "https://missav.com/ja/fc2-ppv-1393190",
        "https://missav.com/ja/fc2-ppv-1393807",
        "https://missav.com/ja/fc2-ppv-1391346",
        "https://missav.com/ja/fc2-ppv-1391490",
        "https://missav.com/ja/fc2-ppv-1388452",
        "https://missav.com/ja/fc2-ppv-1369976",
        "https://missav.com/ja/fc2-ppv-1349465",
        "https://missav.com/ja/fc2-ppv-1352596",
        "https://missav.com/ja/fc2-ppv-1351603",
        "https://missav.com/ja/fc2-ppv-1338025",
        "https://missav.com/ja/fc2-ppv-1335499",
        "https://missav.com/ja/fc2-ppv-1332513",
        "https://missav.com/ja/fc2-ppv-1326465",
        "https://missav.com/ja/fc2-ppv-1311196",
        "https://missav.com/ja/fc2-ppv-1309097",
        "https://missav.com/ja/fc2-ppv-1308835",
        "https://missav.com/ja/fc2-ppv-1314340",
        "https://missav.com/ja/fc2-ppv-1318744",
        "https://missav.com/ja/fc2-ppv-1304833",
        "https://missav.com/ja/fc2-ppv-1305315",
        "https://missav.com/ja/fc2-ppv-1301362",
        "https://missav.com/ja/fc2-ppv-1297587",
        "https://missav.com/ja/fc2-ppv-1288252",
        "https://missav.com/ja/fc2-ppv-1285772",
        "https://missav.com/ja/fc2-ppv-1217541",
        "https://missav.com/ja/fc2-ppv-1220686",
        "https://missav.com/ja/fc2-ppv-1221330",
        "https://missav.com/ja/fc2-ppv-2217427",
        "https://missav.com/ja/fc2-ppv-1212238",
        "https://missav.com/ja/fc2-ppv-1211337",
        "https://missav.com/ja/heyzo-1761",
        "https://missav.com/ja/heyzo-2342",
        "https://missav.com/ja/fc2-ppv-1204323",
        "https://missav.com/ja/fc2-ppv-1207415",
        "https://missav.com/ja/fc2-ppv-1206134",
        "https://missav.com/ja/fc2-ppv-1207169",
        "https://missav.com/ja/fc2-ppv-1205538",
        "https://missav.com/ja/fc2-ppv-1205784",
        "https://missav.com/ja/fc2-ppv-1205683",
        "https://missav.com/ja/fc2-ppv-1201807",
        "https://missav.com/ja/fc2-ppv-1202075",
        "https://missav.com/ja/fc2-ppv-1200439",
        "https://missav.com/ja/fc2-ppv-1199928",
        "https://missav.com/ja/fc2-ppv-1200179",
        "https://missav.com/ja/fc2-ppv-1198912",
        "https://missav.com/ja/fc2-ppv-1196531",
        "https://missav.com/ja/fc2-ppv-934279",
        "https://missav.com/ja/fc2-ppv-1194478",
        "https://missav.com/ja/fc2-ppv-1194669",
        "https://missav.com/ja/fc2-ppv-3161766",
        "https://missav.com/ja/fc2-ppv-3184536",
        "https://missav.com/ja/fc2-ppv-1122370",
        "https://missav.com/ja/fc2-ppv-1122990",
        "https://missav.com/ja/fc2-ppv-1119732",
        "https://missav.com/ja/fc2-ppv-1114306",
        "https://missav.com/ja/fc2-ppv-2892243",
        "https://missav.com/ja/fc2-ppv-2770957",
        "https://missav.com/ja/fc2-ppv-3241576",
        "https://missav.com/ja/fc2-ppv-3138440",
        "https://missav.com/ja/fc2-ppv-1837582",
        "https://missav.com/ja/fc2-ppv-3188064",
        "https://missav.com/ja/fc2-ppv-2552104",
        "https://missav.com/ja/fc2-ppv-3171422",
        "https://missav.com/ja/fc2-ppv-2468011",
        "https://missav.com/ja/fc2-ppv-1324134",
        "https://missav.com/ja/heyzo-0408",
        "https://missav.com/ja/n1082",
        "https://missav.com/ja/fc2-ppv-1586903",
        "https://missav.com/ja/fc2-ppv-1946374",
        "https://missav.com/ja/fc2-ppv-2111364",
        "https://missav.com/ja/fc2-ppv-2089807",
        "https://missav.com/ja/fc2-ppv-798194",
        "https://missav.com/ja/fc2-ppv-1136021",
        "https://missav.com/ja/fc2-ppv-3053224",
        "https://missav.com/ja/fc2-ppv-3191125",
        "https://missav.com/ja/fc2-ppv-2770464",
        "https://missav.com/ja/fc2-ppv-3123185",
        "https://missav.com/ja/fc2-ppv-3218444",
        "https://missav.com/ja/fc2-ppv-2345223",
        "https://missav.com/ja/heyzo-1037",
        "https://missav.com/ja/fc2-ppv-1284607",
        "https://missav.com/ja/fc2-ppv-2092512",
        "https://missav.com/ja/fc2-ppv-1956083",
        "https://missav.com/ja/fc2-ppv-2546182",
        "https://missav.com/ja/fc2-ppv-2661854",
        "https://missav.com/ja/fc2-ppv-2985253",
        "https://missav.com/ja/fc2-ppv-3175412",
        "https://missav.com/ja/fc2-ppv-3137990",
        "https://missav.com/ja/fc2-ppv-3199119",
        "https://missav.com/ja/fc2-ppv-3195661",
        "https://missav.com/ja/fc2-ppv-3181466",
        "https://missav.com/ja/fc2-ppv-3179187",
        "https://missav.com/ja/fc2-ppv-3187452",
        "https://missav.com/ja/fc2-ppv-3053290",
        "https://missav.com/ja/fc2-ppv-2860703",
        "https://missav.com/ja/fc2-ppv-3064646",
        "https://missav.com/ja/111517-002",
        "https://missav.com/ja/fc2-ppv-3039940",
        "https://missav.com/ja/072517-467",
        "https://missav.com/ja/siro-4174",
        "https://missav.com/ja/fc2-ppv-1863914",
        "https://missav.com/ja/042818-01",
        "https://missav.com/ja/heyzo-0168",
        "https://missav.com/ja/041420-283",
        "https://missav.com/ja/fc2-ppv-3136504",
        "https://missav.com/ja/fc2-ppv-3080194",
        "https://missav.com/ja/fc2-ppv-2672887",
        "https://missav.com/ja/zsd-074-uncensored-leak",
        "https://missav.com/ja/fc2-ppv-2051731",
        "https://missav.com/ja/fc2-ppv-3166039",
        "https://missav.com/ja/fc2-ppv-3183038",
        "https://missav.com/ja/sun-041",
        "https://missav.com/ja/rki-165",
        "https://missav.com/ja/fc2-ppv-1313885",
        "https://missav.com/ja/mfcs-039",
        "https://missav.com/ja/fc2-ppv-3007463",
        "https://missav.com/ja/fc2-ppv-3163926",
        "https://missav.com/ja/fc2-ppv-3108774",
        "https://missav.com/ja/fc2-ppv-3144027",
        "https://missav.com/ja/fc2-ppv-3127193",
        "https://missav.com/ja/fc2-ppv-3093895",
        "https://missav.com/ja/fc2-ppv-3177994",
        "https://missav.com/ja/fc2-ppv-1602707",
        "https://missav.com/ja/fc2-ppv-3119206",
        "https://missav.com/ja/fc2-ppv-1912367",
        "https://missav.com/ja/fc2-ppv-1049590",
        "https://missav.com/ja/fc2-ppv-1049143",
        "https://missav.com/ja/fc2-ppv-1046858",
        "https://missav.com/ja/fc2-ppv-1042704",
        "https://missav.com/ja/fc2-ppv-1043734",
        "https://missav.com/ja/fc2-ppv-1042028",
        "https://missav.com/ja/fc2-ppv-1040181",
        "https://missav.com/ja/fc2-ppv-879586",
        "https://missav.com/ja/082918-326",
        "https://missav.com/ja/fc2-ppv-1041285",
        "https://missav.com/ja/fc2-ppv-1094801",
        "https://missav.com/ja/fc2-ppv-1509608",
        "https://missav.com/ja/fc2-ppv-1021461",
        "https://missav.com/ja/fc2-ppv-1021330",
        "https://missav.com/ja/fc2-ppv-1020777",
        "https://missav.com/ja/fc2-ppv-1020757",
        "https://missav.com/ja/fc2-ppv-1019002",
        "https://missav.com/ja/fc2-ppv-1017794",
        "https://missav.com/ja/fc2-ppv-1015441",
        "https://missav.com/ja/fc2-ppv-1016508",
        "https://missav.com/ja/fc2-ppv-1011795",
        "https://missav.com/ja/fc2-ppv-999524",
        "https://missav.com/ja/fc2-ppv-996318",
        "https://missav.com/ja/fc2-ppv-996933",
        "https://missav.com/ja/fc2-ppv-991287",
        "https://missav.com/ja/fc2-ppv-991291",
        "https://missav.com/ja/fc2-ppv-991364",
        "https://missav.com/ja/fc2-ppv-990175",
        "https://missav.com/ja/fc2-ppv-986183",
        "https://missav.com/ja/fc2-ppv-983448",
        "https://missav.com/ja/fc2-ppv-980413",
        "https://missav.com/ja/fc2-ppv-974606",
        "https://missav.com/ja/fc2-ppv-973659",
        "https://missav.com/ja/fc2-ppv-970404",
        "https://missav.com/ja/fc2-ppv-968781",
        "https://missav.com/ja/fc2-ppv-966500",
        "https://missav.com/ja/fc2-ppv-966922",
        "https://missav.com/ja/fc2-ppv-965911",
        "https://missav.com/ja/fc2-ppv-963343",
        "https://missav.com/ja/fc2-ppv-961209",
        "https://missav.com/ja/fc2-ppv-961111",
        "https://missav.com/ja/fc2-ppv-959144",
        "https://missav.com/ja/fc2-ppv-3171718",
        "https://missav.com/ja/fc2-ppv-958337",
        "https://missav.com/ja/fc2-ppv-951724",
        "https://missav.com/ja/fc2-ppv-950267",
        "https://missav.com/ja/fc2-ppv-946670",
        "https://missav.com/ja/fc2-ppv-920821",
        "https://missav.com/ja/021014-540",
        "https://missav.com/ja/fc2-ppv-3093436",
        "https://missav.com/ja/fc2-ppv-939873",
        "https://missav.com/ja/fc2-ppv-937161",
        "https://missav.com/ja/fc2-ppv-932222",
        "https://missav.com/ja/fc2-ppv-920843",
        "https://missav.com/ja/fc2-ppv-916951",
        "https://missav.com/ja/fc2-ppv-878813",
        "https://missav.com/ja/fc2-ppv-901359",
        "https://missav.com/ja/fc2-ppv-883330",
        "https://missav.com/ja/fc2-ppv-881581",
        "https://missav.com/ja/052022-001",
        "https://missav.com/ja/fc2-ppv-855043",
        "https://missav.com/ja/fc2-ppv-816829",
        "https://missav.com/ja/fc2-ppv-809947",
        "https://missav.com/ja/fc2-ppv-803681",
        "https://missav.com/ja/fc2-ppv-767210",
        "https://missav.com/ja/fc2-ppv-767324",
        "https://missav.com/ja/fc2-ppv-735383",
        "https://missav.com/ja/fc2-ppv-702535",
        "https://missav.com/ja/fc2-ppv-776297",
        "https://missav.com/ja/fc2-ppv-777416",
        "https://missav.com/ja/fc2-ppv-770997",
        "https://missav.com/ja/fc2-ppv-769759",
        "https://missav.com/ja/fc2-ppv-584345",
        "https://missav.com/ja/fc2-ppv-653825",
        "https://missav.com/ja/fc2-ppv-619827",
        "https://missav.com/ja/fc2-ppv-577011",
        "https://missav.com/ja/fc2-ppv-578890",
        "https://missav.com/ja/fc2-ppv-555173",
        "https://missav.com/ja/fc2-ppv-559226",
        "https://missav.com/ja/fc2-ppv-553640",
        "https://missav.com/ja/fc2-ppv-549757",
        "https://missav.com/ja/fc2-ppv-524823",
        "https://missav.com/ja/fc2-ppv-505073",
        "https://missav.com/ja/fc2-ppv-490716",
        "https://missav.com/ja/fc2-ppv-485676",
        "https://missav.com/ja/hnd-189",
        "https://missav.com/ja/fc2-ppv-398078",
        "https://missav.com/ja/fc2-ppv-402422",
        "https://missav.com/ja/fc2-ppv-419792",
        "https://missav.com/ja/fc2-ppv-393222",
        "https://missav.com/ja/fc2-ppv-376733",
        "https://missav.com/ja/fc2-ppv-339649",
        "https://missav.com/ja/fc2-ppv-302863",
        "https://missav.com/ja/fc2-ppv-308529",
    ]
    # log.info(video_tag_split_list[4])
    saved_tag_count_dict = {}
    for each_url in video_url_list:
        each_url_info = db.read(where=f"video_url = '{each_url}'")
        if len(each_url_info) > 0:
            saved_id = each_url_info[0][0]
            saved_tag_list = video_tag_split_list[saved_id - 1]
            # log.info(f"{each_url}\n{each_url_info[0][5]}\n{saved_tag_list}")
            for each_tag in saved_tag_list:
                if saved_tag_count_dict.get(each_tag):
                    saved_tag_count_dict[each_tag] += 1
                else:
                    saved_tag_count_dict[each_tag] = 1
            # log.info(f"{each_url}\n{each_url_info[0][5]}\n{saved_tag_list}")
    # log.info(f"{saved_tag_count_dict}")

    # calculate saved tag sum
    value_sum = 0
    saved_tags_weigth_dict = {}
    for key, value in saved_tag_count_dict.items():
        if key != "":
            value_sum += value
    for key, value in saved_tag_count_dict.items():
        tag_weight = round(value / value_sum * 1000, 3)
        log.info(f"{key}{tag_weight}")
        saved_tags_weigth_dict[key] = tag_weight

    # modify tag weight
    for key, value in video_tags_weigth_dict.items():
        if saved_tags_weigth_dict.get(key):
            video_tags_weigth_dict[key] = saved_tags_weigth_dict[key]
    log.info(f"{video_tags_weigth_dict}")

    # calculate w score
    for each_tag_list in video_tag_split_list:
        weight_score = 0
        for each_tag in each_tag_list:
            if each_tag != "":
                weight_score += video_tags_weigth_dict[each_tag]
        weight_score = round(weight_score, 3)
        log.info(f"{weight_score}")


def convert_to_halfwidth(input_str):
    result = []
    for char in input_str:
        halfwidth_char = unicodedata.normalize("NFKC", char)
        result.append(halfwidth_char)
    return "".join(result)


def multi_threads(job, thread_quantity=2, job_args=""):
    log.info(f"{sys._getframe().f_code.co_name}")
    threads = []
    # thread start
    for thread_number in range(thread_quantity):
        threads.append(threading.Thread(target=job, args=[job_args, thread_number]))
        threads[thread_number].start()
    # wait all thread finish
    for thread_number in range(thread_quantity):
        threads[thread_number].join()


def line_notify(token, msg):
    log.info(f"{sys._getframe().f_code.co_name}: send message")
    token = test_token
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"message": msg}
    return requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload, timeout=10
    )


if __name__ == "__main__":
    # set logger
    remove_old_log(log_path=log_path, log_name=py_name)
    log = py_logger("w", level="INFO", log_path=log_path, log_name=py_name)

    # set Database
    db_name = py_name
    db_path = f"{py_path}/file/database/{db_name}.sqlite3"
    db = Database(db_path=db_path)
    table = "test_table"
    table_dict = {
        "video_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "video_url": "TEXT",
        "video_number": "TEXT",
        "video_name": "TEXT",
        "video_date": "TEXT",
        "video_tags": "TEXT",
        "last_modified_date": "DATETIME",
    }
    db.create_table(table, table_dict)
    db.use_table(table)
    # db.delete_all()

    # main start
    main()

    # close database
    db.close()

    # close log
    close_log(log)

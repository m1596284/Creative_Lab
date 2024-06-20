# -*- coding: utf-8 -*-
# 2022_0801 v2
import time
import datetime
import bs4
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from py_logging import py_logger, close_log, remove_old_log
from sqlite_CRUD import Database
from lxml import etree


def main():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'content-length': '17373',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'ASP.NET_SessionId=mabdfwvz3drknlcz5qyk1tql',
        'origin': 'https://www.dailyair.com.tw',
        'referer': 'https://www.dailyair.com.tw/Dailyair/Page/WOWP/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    data = {
        # '__EVENTTARGET':'',
        # '__EVENTARGUMENT':'',
        '__VIEWSTATEFIELDCOUNT': '12',
        '__VIEWSTATE': '2uVFFo8P1X9eHxI+eAi0UVtl7tGsYYiIMmOoUqKfpocmUOR2BNDahg/fwi1SOQO0wG8ljzqFekbuvKIczJAKmln3U2z0rnPlVAlC',
        '__VIEWSTATE1': '5Q0t+Yazbkswo4JNXnb18Rs05R2Z78crt9vsHT1ssDr7K/ysw2QxDMP1mSJZ//KOldbEa+XuPfuwXSyHnzDyUDv6JQHzCdzuIPbF',
        '__VIEWSTATE2': 'lWEvVKaOvwdURyAnFZ2ubxeVDHpN26a3gc+ZcoKwzknkH//733kEtxvxIEmjp1uVJFMBo/tpgDPxxlVpQ2SZ2lDANmYSV8gcJKgq',
        '__VIEWSTATE3': 'b2SiB7/xzsU/5loviFTSHtBnno3yZBCOi9YYcpvbuiQov3NKzizZR5DNpOKBqMz1djCa0WGdbFaAIb+kIqerCtutqMqmwJQ3h7n7',
        '__VIEWSTATE4': 'pV64rINHrfJAmk2uLgugT0y3F23HHhAaNlSdVvf1GOvbM/+mJJpezGSr6n4wjNaMxyqAe12tqBq4IL7xtMvcEyWdZa5yCB+Axmvp',
        '__VIEWSTATE5': 'PSkpuCrDOIP36Jjwo3eI+PKais2ESmuyafe+mBIcVSxNxnwJ+kpvhp/Bv0iOpu2jeb5Jwhi7adxfEvUJb2p+9tp9TNO1/Rw18N7J',
        '__VIEWSTATE6': 'Nij+zt7SYfKwo78t1pWjoRTyFgRJEnpxcXFD683L3raZTjqMcxsbaSes/jtTlpKU1FWJQP5KjjXEeYAbb8sxQ0NMcEhKNN7Mploa',
        '__VIEWSTATE7': 'rkvYKX8r2LhaTXLbMbIk24PaFW1tPKvTU4QDhi++cxbTv2I+vH1KC+f8N+eUYSiOBLh7Bx+XUHFHfZ8YzTByWbHIpCqAMniEdqC+',
        '__VIEWSTATE8': 'R+DhsT9zQQvHE6WTpWMF3qI0djWKaVps4enL9c1HWD4kpS9aP9QqTuojABWp4oQNngCeyl39Lgth18PCFUciJy7upuc2hxWqjupg',
        '__VIEWSTATE9': 'EQhhudx4LtJfruZaI6IyNSFdaX6IVeq+/8BF9/nY5OwuRH1d3IT4Y8BzQ8Q5MWcMB2Q6jo0ZAg28DJn20uZOUaU+Fp8+dIiizvk4',
        '__VIEWSTATE10': '3NTsJO8+yiN+F7+Md/GQSBAucRUpLRrVNTdcB0NJNatTJg50i75xGpbxkiG7nIutWM2/+GvO2amfCs2Iklo5F56VfnxEou6Qc1UR',
        '__VIEWSTATE11': 'ZrDHAkQnloDJZrpG6Aj8HqFkL8gtAz14JmclblIjoezADTEOuNxUSprJDc4A1WR9ZYDtinXbSQ==',
        # '__VIEWSTATEGENERATOR':'D78D7CCB',
        # '__VIEWSTATEENCRYPTED':'',
        '__EVENTVALIDATION': 'H5kZyMyO1F+Go4HcJzv6Ruf0ghyVJDC3Q85F0+CRkbacgLYo//i3mr6tKaEIIG1eFMJthJTLXbadEGmymx4A1lv1Fv6TRYtqarcXf0ZVBaNXfjcvryl6QTnKFbosaqf96partdtrlrtk9PxxNAiVAvwUyNq9Acb45I+3tbqvGSVF+oIYvgURgrROZdVbezTramZUqKWFR9xS7uPQ5V8tgenoObM0jSIdoaP3zcRAQImgQn6po2yZlS/FuPtyOs4momc4gEVG55e9+3m7D540PU+BAzgs83Z4eK1haLtctId/Kc0GYQNch+RaVsFfbQrpcJ1QUHAx5DUHI8Mdwmj6OwPS7dKXoaCQxuad8SbjSNttmglSj90ozxPeXe3IYZVp2EOBZRqi2GFuctOU+fXe8LSfOHLKZYBwTBmOpdl988qNH6MQCMvFWmmikc0dKkKcJu1EYwhudoIC5IkUeMWKyj1Xr4PUh42iYxXNbVqX0zeVXLKbFeg1BFuS5zUdLfX4ii+dKqfhxLTiKAh39kcRpq3yxwPan8I9VYs6VdOozY14LWL9lqgnoGCq3+/qZqM/KSWGHs3Yzb0OtCt4OZ5eVc8ykcUYoqg+ix2zuUGIT6JNklBA85FQJxTAC8OxMO5jC02smiHdDx8W16RxdvPlFRYZhA0xcLRxV4Ea6NGMzGO5LZNINTTVD4CzuZsBw+ZZ4GRQU9pkYy4fbDSPin3Fmw==',
        # 'ctl00$hid_news':'',
        'ctl00$BodyContent$ctl00$_Key': '03ANYolquTO8BdRms0JaHBSEyoVK-vS-7nP-fBGD2u9HIDrhCvxMuDKgGG75vxE86EY0F-BBNV-lABM7rHK94zey6DYosfViZHX7tLaEIUiZeC_T7qcwW2Prb542w4vJOKde8QqClRlUhxSwl57eVxi4t27uI6XXWndBpQGjJCCMRnhfVCQrRFHiJGKPhOKu35DsDv3WXU-rPUV_SZk3ejTHHrbgi28VrVITzHOBUxXGaXpYtCFc7vrhNAl73IPc9BcZrXLuK66skvgoXyxjGyTIQzZpwd8M1Gs20BBjl-_MdiD2YAhlbgvcBpbJYya-N9VuFN4QwF4IUbz3uC3oOtjDympDMtaNwSJbl7j52P4vq1dX-MMkiqzMPsGzCiEVxfI-2nNOWCVx8FOmrkSZpGsN5FHvYFpEc6qy7texQNLksdnk-t6Mj1QJi9OD4Mm4Xozhgq0bmRieRSAgJB6Zs8fv3jNr0UR0N4D9IqYp9uH6lzy8XozeVtizKBgddO9DQPuybs1pXbJ444',
        'ctl00$BodyContent$ctl00$wowp_hid_AirlineName': '台東（TTT） - 蘭嶼（KYD）',
        'ctl00$BodyContent$ctl00$wowp_sel_Airline': '4',
        'ctl00$BodyContent$ctl00$wowp_radio_goback': '1',
        'ctl00$BodyContent$ctl00$wowp_hid_GoTripDate': f'2022/{go_date}',
        'ctl00$BodyContent$ctl00$wowp_hid_BackTripDate': f'2022/{back_date}',
        'ctl00$BodyContent$ctl00$wowp_sel_Passengers': '4',
        'ctl00$BodyContent$ctl00$wowp_cb_notice': 'on',
        'ctl00$BodyContent$FlightQuery': '航 班 查 詢',
    }
    r = requests.post(page_url, headers=headers, data=data)
    soup = BeautifulSoup(r.text, 'html.parser')
    log.info(soup)
    go_query = soup.find_all(
        'table', id="BodyContent_ctl00_go_wowp_tbe_flight_query")
    back_query = soup.find_all(
        'table', id="BodyContent_ctl00_back_wowp_tbe_flight_query")
    go_list = []
    log.info(go_query)
    for num, thing in enumerate(go_query[0].tbody):
        if num != 0 and num < 9:
            for num_2, col in enumerate(thing):
                if num_2 == 1:
                    go_list.append(col.get_text())
                if num_2 == 5:
                    go_list.append(col.get_text())
    # log.info(go_list)
    back_list = []
    for num, thing in enumerate(back_query[0].tbody):
        if num != 0 and num < 9:
            for num_2, col in enumerate(thing):
                if num_2 == 1:
                    back_list.append(col.get_text())
                if num_2 == 5:
                    back_list.append(col.get_text())
    # log.info(back_list)
    if "尚餘" in go_list[11] or "尚餘" in go_list[13]:
        msg = f'\n去程有空位\n{go_date}\nhttps://www.dailyair.com.tw/Dailyair/Page/WOWP/'
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify",
                          headers=headers, params=payload)
    if "尚餘" in back_list[11] or "尚餘" in back_list[13] or "尚餘" in back_list[15]:
        msg = f'\n回程有空位\n{back_date}\nhttps://www.dailyair.com.tw/Dailyair/Page/WOWP/'
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify",
                          headers=headers, params=payload)


if __name__ == "__main__":
    # set path and name
    here_dir = Path(__file__).parent
    py_name = Path(__file__).stem

    # set logger
    remove_old_log(log_path=f"{here_dir}/log", file_name=py_name)
    log = py_logger("w", level="INFO",
                    log_path=f"{here_dir}/log", file_name=py_name)

    page_url = "https://www.dailyair.com.tw/Dailyair/Page/WOWP/"
    go_date = "10/23"
    back_date = "10/24"
    msg = f'\nstart'
    token = "ppe8qq75KOiH87Rv1Zn6oYqXI0EfU7odbGLIHXUUCaj"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)

    while True:
        # start test
        log.info(f"keep running")
        main()
        time.sleep(5)

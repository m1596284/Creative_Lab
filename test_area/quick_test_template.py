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
from selenium import webdriver

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

if __name__ == "__main__":
    pass

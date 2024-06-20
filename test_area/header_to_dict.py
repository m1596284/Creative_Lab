# -*- coding: utf-8 -*-
# 2023_0702 v3

from pathlib import Path
from py_logging import py_logger, close_log, remove_old_log

# set path and name
py_name = Path(__file__).stem
py_path = Path(__file__).parent
log_path = f"{py_path}/log"
log = py_logger("w", level="INFO", log_path=log_path, log_name=py_name)

with open(f"{str(py_path)}/headers.txt", encoding="utf-8") as f:
    header_lines = f.readlines()
headers = "{\n"
for line_num, line_string in enumerate(header_lines):
    log.info(line_num)
    if line_num % 2 == 0:
        key = line_string.replace("\n", "").replace(":", "").strip()
    if line_num % 2 == 1:
        value = line_string.replace("\n", "").strip()
        headers = f"{headers}    '{key}':'{value}',\n"
headers = headers + "}"
with open(f"{str(py_path)}/headers.txt", "w", encoding="utf-8") as f:
    f.write(headers)

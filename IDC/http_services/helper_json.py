import json
from traceback import print_tb

import pandas as pd
import re
import time
from decimal import Decimal
def json_decode(json_file_path):
    with open(json_file_path, 'r', encoding='raw_unicode_escape') as f:
        json_content = f.read()
        json_content = json.loads(json_content)
        json_content = json.dumps(json_content)
        json_content = json_content.encode('raw_unicode_escape').decode('utf-8')
        json_content = json.loads(json_content)
    return json_content['Data']

def helper1(data,selected_points):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    raw_data_triple = [(timestamp, pid, next((Decimal(item["curvalue"]) for item in data if item["property_id"] == pid), "N/A"))
              for pid in selected_points]
    data_dict = {item["property_id"]: Decimal(item["curvalue"]) for item in data}
    raw_data_dict = {pid: data_dict.get(pid, "N/A") for pid in selected_points}

    return raw_data_triple, raw_data_dict

content = json_decode('C:\\Users\\32652\\Desktop\\partime\\翔明科技\\IDC\\output.json')
pids = [item["property_id"] for item in content]

a,b=helper1(content, pids[0:100])

print(type(content))

import json
import pandas as pd
import re


def json_decode(json_file_path):
    with open(json_file_path, 'r', encoding='raw_unicode_escape') as f:
        json_content = f.read()
        json_content = json_content.encode('raw_unicode_escape').decode('utf-8')
    return json_content


content = json_decode('C:\\Users\\32652\\Desktop\\partime\\翔明科技\\IDC\\output.json')

dict = json.loads(content)
print(dict)

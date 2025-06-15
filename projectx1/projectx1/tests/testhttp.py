import json
import time
import src.utils.http as hp
import src.config as con

if __name__ == '__main__':
    # 测试数据接口
    for k, api in con.GET_API.items():
        test_url = con.PRODUCTION_URL + api
        response = hp.get_data(url=test_url)
        print(response)

    # 测试预测接口
    for k, api in con.POST_API.items():
        test_url = con.PRODUCTION_URL + api
        json_data = con.POST_PARAMS[k]['json_data']

        response = hp.post_forecast(url=test_url, params=None, json=json_data)
        print(response)

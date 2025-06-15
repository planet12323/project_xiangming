import json

import requests


def get_data(url, params=None, headers=None):
    try:
        headers={
            'apiKey': '1234567890'
        }
        data = json.dumps(params)
        response = requests.get(url, data=None, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"GET请求出错: {e}")
        return None


def post_forecast(url, params=None, json=None, headers=None):
    try:
        headers = {
            'apiKey': '1234567890'
        }
        response = requests.post(url, params=params, json=json, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"POST请求出错: {e}")
        return None

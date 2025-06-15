import requests


def get_device_list(url='http://192.168.1.246:10088/api/GetDeviceList', keys=""):
    """
    获取设备配置信息
    :param url: 获取数据地址
    :param keys: 关键字，为空时查询所有设备配置信息；不为空时匹配设备id、设备名称
    :return: 设备配置信息列表
    """
    payload = {"keys": keys}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查请求是否成功

        data = response.json()
        if data.get("Status") == "ok":
            return data.get("Data", [])
        else:
            print(f"请求失败: {data.get('Message', '未知错误')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return []


def get_real_time_data(url = 'http://192.168.1.246:10088/api/GetRealTimeData', device_ids=None, property_ids=None):
    """
    获取设备监控参数实时值
    :param url: 获取数据地址
    :param device_ids: 设备id集合；可为None，为None时获取所有设备参数实时值
    :param property_ids: 参数ID集合；可为None，或者指定参数ID
    :return: 设备监控参数实时值列表
    """

    # 处理参数为None的情况
    if device_ids is None:
        device_ids = []
    if property_ids is None:
        property_ids = []

    payload = {
        "device_ids": device_ids,
        "property_ids": property_ids
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查请求是否成功

        data = response.json()
        if data.get("Status") == "ok":
            return data.get("Data", [])
        else:
            print(f"请求失败: {data.get('Message', '未知错误')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return []


def send_command(url='https://139.129.89.24/niagara/xm/tms/device/setControlPoints', commands=None):
    """
    发送控制命令到指定设备
    :param url: 控制命令发送地址
    :param commands: 控制命令字典，包含具体控制参数
    :return: 返回服务器响应的数据或空列表
    """
    if not isinstance(commands, dict):
        print("无效的命令格式: commands 参数必须是字典")
        return []

    try:
        response = requests.post(url, json=commands)
        response.raise_for_status()  # 检查请求是否成功

        data = response.json()
        if data.get("Status") == "ok":
            return data.get("Data", [])
        else:
            print(f"请求失败: {data.get('Message', '未知错误')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return []


# 示例用法
if __name__ == "__main__":
    # 获取所有设备配置
    all_devices = get_device_list()
    print(f"获取到 {len(all_devices)} 个设备配置")

    # 获取指定设备的实时数据
    if all_devices:
        device_ids = [device["device_id"] for device in all_devices[:2]]  # 取前两个设备
        real_time_data = get_real_time_data(device_ids=device_ids)
        print(f"获取到 {len(real_time_data)} 条实时数据")
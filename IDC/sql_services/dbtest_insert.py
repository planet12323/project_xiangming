import psycopg2
import random
import json
from datetime import datetime, timedelta
import string

# 数据库连接信息
DB_HOST = "localhost"
DB_NAME = "your_database_name"
DB_USER = "your_username"
DB_PASSWORD = "your_password"

# 连接到数据库
conn = psycopg2.connect(
    database="xiangmingtest",
    user="postgres",
    password="000000",
    host="127.0.0.1",
    port="5432"
)

cursor = conn.cursor()

property_idx = list()
command_idx=list()
analysis_idx=list()

# 辅助函数：生成随机字符串
def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 辅助函数：生成随机时间戳
def random_timestamp(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# 辅助函数：生成随机JSON数据
def random_json(keys, value_type="float"):
    data = {}
    for key in keys:
        if value_type == "float":
            data[key] = round(random.uniform(0, 100), 2)
        elif value_type == "int":
            data[key] = random.randint(0, 100)
    return json.dumps(data)

# 生成测试数据
def generate_test_data():
    # 定义时间范围
    start_time = datetime(2024, 1, 1)
    end_time = datetime.now()

    # point_info 表
    for i in range(200):
        property_id = random_string(16)
        property_idx.append(property_id)
        property_name = random_string(32)
        device_id = random_string(16)
        device_name = random_string(32)
        category_name = random.choice(["Category1", "Category2", "Category3"])
        area_name = random.choice(["Area1", "Area2", "Area3"])
        value_unit = random.choice(["°C", "kW", "m³/h"])
        value_symbol = random.choice(["+", "-", "*", "/"])
        status = random.choice(["Active", "Inactive", "Pending"])
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO point_info (property_id, property_name, device_id, device_name, category_name, area_name, value_unit, value_symbol, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (property_id, property_name, device_id, device_name, category_name, area_name, value_unit, value_symbol, status)
        )

    # raw_collected_data 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        property_id = property_idx[i]  # 假设 property_id 已存在
        data_value = round(random.uniform(0, 1000), 5)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO raw_collected_data (time_stamp, property_id, data_value)
            VALUES (%s, %s, %s)
            """,
            (time_stamp, property_id, data_value)
        )

    # command_info 表
    for i in range(200):
        command_id = random_string(16)
        command_idx.append(command_id)
        command_name = random_string(32)
        command_formula = random_string(128)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO command_info (command_id, command_name, command_formula)
            VALUES (%s, %s, %s)
            """,
            (command_id, command_name, command_formula)
        )

    # command_data 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        command_id = command_idx[i]  # 假设 command_id 已存
        command_value = round(random.uniform(0, 1000), 5)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO command_data (time_stamp, command_id, command_value)
            VALUES (%s, %s, %s)
            """,
            (time_stamp, command_id, command_value)
        )

    # analysis_info 表
    for i in range(200):
        analysis_id = random_string(16)
        analysis_idx.append(analysis_id)
        analysis_name = random_string(32)
        analysis_formula = random_string(128)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO analysis_info (analysis_id, analysis_name, analysis_formula)
            VALUES (%s, %s, %s)
            """,
            (analysis_id, analysis_name, analysis_formula)
        )

    # display_results 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        selected_points = random_json(["point1", "point2", "point3"])
        cal_method = random.choice(["Entropy", "Average", "Max"])
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO display_results (time_stamp, selected_points, cal_method)
            VALUES (%s, %s, %s)
            """,
            (time_stamp, selected_points, cal_method)
        )

    # manual_parameters 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        supply_temp_upper = round(random.uniform(0, 100), 2)
        return_temp_lower = round(random.uniform(0, 100), 2)
        unit_flow = random_json(["L-1", "L-2", "L-3"])
        cal_frequency = random.randint(1, 60)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO manual_parameters (time_stamp, supply_temp_upper, return_temp_lower, unit_flow, cal_frequency)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (time_stamp, supply_temp_upper, return_temp_lower, unit_flow, cal_frequency)
        )

    # analysis_results 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        analysis_id = analysis_idx[i] # 假设 analysis_id 已存在
        analysis_value = round(random.uniform(0, 1000), 5)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO analysis_results (time_stamp, analysis_id, analysis_value)
            VALUES (%s, %s, %s)
            """,
            (time_stamp, analysis_id, analysis_value)
        )

    # hourly_analysis 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        device_selection = random_string(32)
        parameter_selection = random_string(32)
        analysis_value = round(random.uniform(0, 1000), 5)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO hourly_analysis (time_stamp, device_selection, parameter_selection, analysis_value)
            VALUES (%s, %s, %s, %s)
            """,
            (time_stamp, device_selection, parameter_selection, analysis_value)
        )

    # daily_analysis 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        device_selection = random_string(32)
        parameter_selection = random_string(32)
        analysis_value = round(random.uniform(0, 1000), 5)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO daily_analysis (time_stamp, device_selection, parameter_selection, analysis_value)
            VALUES (%s, %s, %s, %s)
            """,
            (time_stamp, device_selection, parameter_selection, analysis_value)
        )

    # monthly_analysis 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        device_selection = random_string(32)
        parameter_selection = random_string(32)
        analysis_value = round(random.uniform(0, 1000), 5)
        created_at = random_timestamp(start_time, end_time)
        cursor.execute(
            """
            INSERT INTO monthly_analysis (time_stamp, device_selection, parameter_selection, analysis_value)
            VALUES (%s, %s, %s, %s)
            """,
            (time_stamp, device_selection, parameter_selection, analysis_value)
        )

    # yearly_analysis 表
    for i in range(200):
        time_stamp = random_timestamp(start_time, end_time)
        device_selection = random_string(32)
        parameter_selection = random_string(32)
        analysis_value = round(random.uniform(0, 1000), 5)
        created_at = random_timestamp(start_time, end_time)

        cursor.execute(
            """
            INSERT INTO yearly_analysis (time_stamp, device_selection, parameter_selection, analysis_value)
            VALUES (%s, %s, %s, %s)
            """,
            (time_stamp, device_selection, parameter_selection, analysis_value)
        )

        # 提交事务
    conn.commit()
    print("测试数据插入完成！")


# 调用函数生成测试数据
generate_test_data()

# 关闭数据库连接
cursor.close()
conn.close()
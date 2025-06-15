from collections import defaultdict

import numpy as np
import pandas as pd
import psycopg2
from psycopg2 import pool
from psycopg2 import extras
import contextlib


DB_CONFIG = {
    'dbname': 'xiangmingtest',
    'user': 'postgres',
    'password': '000000',
    'host': '127.0.0.1',
    'port': 5432
}

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)


@contextlib.contextmanager
def get_db_connection():
    """从连接池获取连接，并在使用后释放回池"""
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)


def update_raw_collected_data(data):
    """data = [(time_stamp, property_id, data_value)]"""
    query = "INSERT INTO raw_collected_data (time_stamp, property_id, data_value) VALUES (%s, %s, %s)"
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_point_info(data):
    """
    批量更新point_info表
    data = [(property_id, property_name, device_id, device_name, category_name, area_name, value_unit, value_symbol, status)]
    """
    query = """
        INSERT INTO point_info (
            property_id, property_name, device_id, device_name, 
            category_name, area_name, value_unit, value_symbol, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_command_info(data):
    """
    批量更新command_info表
    data = [(command_id, command_name, command_formula)]
    """
    query = """
        INSERT INTO command_info (command_id, command_name, command_formula)
        VALUES (%s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_command_data(data):
    """
    批量更新command_data表
    data = [(time_stamp, command_id, command_value)]
    """
    query = """
        INSERT INTO command_data (time_stamp, command_id, command_value)
        VALUES (%s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_analysis_info(data):
    """
    批量更新analysis_info表
    data = [(analysis_id, analysis_name, analysis_formula)]
    """
    query = """
        INSERT INTO analysis_info (analysis_id, analysis_name, analysis_formula)
        VALUES (%s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_display_results(data):
    """
    批量更新display_results表
    data = [(time_stamp, selected_points, cal_method)]
    """
    query = """
        INSERT INTO display_results (time_stamp, selected_points, cal_method)
        VALUES (%s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_manual_parameters(data):
    """
    批量更新manual_parameters表
    data = [(time_stamp, supply_temp_upper, return_temp_lower, unit_flow, cal_frequency)]
    """
    query = """
        INSERT INTO manual_parameters (
            time_stamp, supply_temp_upper, return_temp_lower, unit_flow, cal_frequency
        ) VALUES (%s, %s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_analysis_results(data):
    """
    批量更新analysis_results表
    data = [(time_stamp, analysis_id, analysis_value)]
    """
    query = """
        INSERT INTO analysis_results (time_stamp, analysis_id, analysis_value)
        VALUES (%s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_hourly_analysis(data):
    """
    批量更新hourly_analysis表
    data = [(time_stamp, device_selection, parameter_selection, analysis_value)]
    """
    query = """
        INSERT INTO hourly_analysis (time_stamp, device_selection, parameter_selection, analysis_value)
        VALUES (%s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_daily_analysis():
    """
    批量更新daily_analysis表
    data = [(time_stamp, device_selection, parameter_selection, analysis_value)]
    """
    data=[]
    query = """
        INSERT INTO daily_analysis (time_stamp, device_selection, parameter_selection, analysis_value)
        VALUES (%s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_monthly_analysis(data):
    """
    批量更新monthly_analysis表
    data = [(time_stamp, device_selection, parameter_selection, analysis_value)]
    """
    query = """
        INSERT INTO monthly_analysis (time_stamp, device_selection, parameter_selection, analysis_value)
        VALUES (%s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_yearly_analysis(data):
    """
    批量更新yearly_analysis表
    data = [(time_stamp, device_selection, parameter_selection, analysis_value, unit)]
    """
    query = """
        INSERT INTO yearly_analysis (time_stamp, device_selection, parameter_selection, analysis_value, unit)
        VALUES (%s, %s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                extras.execute_batch(cursor, query, data, page_size=100)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def update_model_input(vars):
    query = f"""
            INSERT INTO model_input ( time_stamp, qcooling, tin, pit, outdoor, tsupply, tset)
            VALUES (%s, %s, %s, %s, %s, %s, %s) \
            """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, vars)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def get_point_info_except_Tin() -> dict:
    """
    根据property_id查询point_info表中的单条记录
    返回字典格式：{'property_id': ..., 'property_name': ..., ...}
    """
    query = """
        SELECT property_id FROM point_info 
        WHERE value_symbol != 'Tin'
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_command_info() -> list:
    """
    分页查询command_info表中的记录
    返回字典列表：[{'command_id': ..., 'command_name': ..., ...}, ...]
    """
    query = """
        SELECT command_id FROM command_info 
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_analysis_info() -> list:
    """
    根据关键词搜索analysis_info表中的记录（模糊匹配analysis_name和analysis_formula）
    返回字典列表：[{'analysis_id': ..., 'analysis_name': ..., ...}, ...]
    """
    query = """
        SELECT analysis_id FROM analysis_info 
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_manual_parameters() -> list:
    query = """
            WITH latest_timestamp AS (
                SELECT MAX(time_stamp) AS max_ts
                FROM manual_parameters
            )
            SELECT supply_temp_upper, return_temp_lower, unit_flow, cal_frequency 
            FROM manual_parameters
            JOIN latest_timestamp ON manual_parameters.time_stamp = latest_timestamp.max_ts
        """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

    '''return [(supply_temp_upper, return_temp_lower, unit_flow, cal_frequency)]'''
    return result if result else None


def get_display_results():
    """
    从display_results表中获取最新时间戳的数据并返回selected_points和cal_method
    返回元组：(selected_points, cal_method)
    """
    query = """
            WITH latest_timestamp AS (SELECT MAX(time_stamp) AS max_ts
                                      FROM display_results)
            SELECT selected_points, cal_method
            FROM display_results
                     JOIN latest_timestamp ON display_results.time_stamp = latest_timestamp.max_ts \
            """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
    return result if result else (None, None)

def get_model_input(step):
    query = f"""
            SELECT * 
            FROM model_input 
            ORDER BY time_stamp DESC 
            LIMIT {step};
            """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    return result if result else None


def get_static_symbol():
    # 查询所有 property_id 和 value_symbol，排除 value_symbol 为 'Tin' 的数据
    query = """
            SELECT property_id, value_symbol
            FROM point_info
            """
    result_dict = defaultdict(list)  # 使用 defaultdict 自动处理键不存在的情况
    Tin = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                # 处理查询结果
                for row in cursor.fetchall():
                    property_id, value_symbol = row
                    # 处理空值，使用 'symbol_unknown' 作为默认键
                    if value_symbol == 'Tin':
                        Tin.append(key)
                        continue
                    key = value_symbol if value_symbol else 'symbol_unknown'
                    result_dict[key].append(property_id)
    finally:
        conn.close()  # 确保数据库连接关闭

    return dict(result_dict), Tin  # 转换为普通字典返回

def get_W():
    query = """
                SELECT property_id, data_value
                FROM raw_collected_data
                WHERE time_stamp = (
                    SELECT MAX(time_stamp) 
                    FROM raw_collected_data
                ) AND property_id in ('EQD05030', 'EQD06030', 'EQD04030', 'EQD03030');
            """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    return result if result else None

if __name__ == '__main__':
    # print(get_point_info())
    # print(get_command_info())
    # print(get_analysis_info())
    W = get_W()
    W_1 = W[0][1]
    W_2 = W[1][1]
    W_3 = W[2][1]
    W_4 = W[3][1]
    print(W_1, W_2, W_3, W_4)

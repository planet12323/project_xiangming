import psycopg2

conn = psycopg2.connect(
    database="xiangmingtest",
    user="postgres",
    password="000000",
    host="127.0.0.1",
    port="5432"
)

commands = [
    {
        "command_id": "TEMP_SUPPLY",
        "command_name": "供水温度",
        "command_formula": "Tsupply=(Tsupply_1+Tsupply_2)/2"
    },
    {
        "command_id": "TEMP_DIFF",
        "command_name": "供回水温差",
        "command_formula": "Δt=Treturn-Tsupply"
    },
    {
        "command_id": "FLOW_L1",
        "command_name": "L-1磁悬浮机组进水流量",
        "command_formula": "G1"
    },
    {
        "command_id": "FLOW_L2",
        "command_name": "L-2磁悬浮机组进水流量",
        "command_formula": "G2"
    },
    {
        "command_id": "FLOW_L3",
        "command_name": "L-3螺杆机组进水流量",
        "command_formula": "G3"
    },
    {
        "command_id": "FLOW_L4",
        "command_name": "L-4螺杆机组进水流量",
        "command_formula": "G4"
    }
]


def insert_commands():
    try:
        # 连接数据库
        cursor = conn.cursor()

        # 插入命令数据
        for cmd in commands:
            insert_query = """
                           INSERT INTO command_info (command_id, command_name, command_formula)
                           VALUES (%s, %s, %s) \
                           """
            cursor.execute(insert_query, (cmd["command_id"], cmd["command_name"], cmd["command_formula"]))

        # 提交事务
        conn.commit()
        print("命令数据插入成功！")

    except (Exception, psycopg2.Error) as error:
        print(f"插入数据时出错: {error}")
    finally:
        # 关闭数据库连接
        conn.close()
insert_commands()
# import psycopg2
# from psycopg2 import sql, extras
# from faker import Faker
# import random
# import uuid
# from datetime import datetime, timedelta
#
# fake = Faker('zh_CN')
#
# # 连接数据库（请修改参数）
# conn = psycopg2.connect(
#     database="xiangmingtest",
#     user="postgres",
#     password="000000",
#     host="127.0.0.1",
#     port="5432"
# )
# cur = conn.cursor()
#
#
# # 生成随机时间戳
# def random_timestamp(days=365):
#     return datetime.now() - timedelta(days=random.randint(0, days))
#
#
# # 生成随机日期
# def random_date(days=365):
#     return (datetime.now() - timedelta(days=random.randint(0, days))).date()
#
#
# # 清空所有表（谨慎使用）
# def truncate_tables():
#     tables = [
#         "yearly_analysis", "analysis_results", "raw_collected_data",
#         "manual_parameters", "point_info", "display_results",
#         "analysis_info", "command_info", "history_trend",
#         "hourly_analysis", "daily_analysis", "command_data", "monthly_analysis"
#     ]
#     for table in tables:
#         cur.execute(sql.SQL("TRUNCATE TABLE {} CASCADE").format(sql.Identifier(table)))
#
#
# # 生成analysis_info表数据
# def generate_analysis_info(count=200):
#     for _ in range(count):
#         analysis_id = f"A{uuid.uuid4().hex[:15]}"
#         analysis_name = f"分析_{fake.word()}"
#         analysis_formula = f"{fake.word()} + {fake.word()} * {random.randint(1, 10)}"
#         created_at = random_timestamp()
#
#         cur.execute(
#             "INSERT INTO analysis_info (analysis_id, analysis_name, analysis_formula, created_at) "
#             "VALUES (%s, %s, %s, %s)",
#             (analysis_id, analysis_name, analysis_formula, created_at)
#         )
#
#
# # 生成point_info表数据
# def generate_point_info(count=200):
#     for _ in range(count):
#         property_id = f"P{uuid.uuid4().hex[:15]}"
#         property_name = f"{fake.word()}_{random.randint(1, 100)}"
#         device_id = f"D{uuid.uuid4().hex[:15]}"
#         device_name = f"设备_{fake.word()}"
#         category_name = random.choice(["温湿度", "电压", "电流", "功率", "频率"])
#         area_name = f"{fake.city()}>>{fake.street_name()}>>{fake.building_number()}"
#         value_unit = random.choice(["℃", "%", "V", "A", "kW", "Hz"])
#         value_symbol = random.choice(["T", "H", "V", "I", "P", "f"])
#         status = random.choice(["正常", "告警", "离线", "维护"])
#         created_at = random_timestamp()
#         remark = fake.sentence()
#
#         cur.execute(
#             "INSERT INTO point_info (property_id, property_name, device_id, device_name, "
#             "category_name, area_name, value_unit, value_symbol, status, created_at, remark) "
#             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#             (property_id, property_name, device_id, device_name,
#              category_name, area_name, value_unit, value_symbol, status, created_at, remark)
#         )
#
#
# # 生成command_info表数据
# def generate_command_info(count=200):
#     for _ in range(count):
#         command_id = f"C{uuid.uuid4().hex[:15]}"
#         command_name = f"命令_{fake.word()}"
#         command_formula = f"{fake.word()} * {random.randint(1, 10)} - {random.randint(1, 5)}"
#         created_at = random_timestamp()
#         execution_mode = random.choice(["自动", "手动", "定时"])
#
#         cur.execute(
#             "INSERT INTO command_info (command_id, command_name, command_formula, created_at, execution_mode) "
#             "VALUES (%s, %s, %s, %s, %s)",
#             (command_id, command_name, command_formula, created_at, execution_mode)
#         )
#
#
# # 生成其他表数据（依赖于前面的表）
# def generate_other_tables(count=200):
#     # 获取已生成的外键值
#     cur.execute("SELECT analysis_id FROM analysis_info")
#     analysis_ids = [row[0] for row in cur.fetchall()]
#
#     cur.execute("SELECT property_id FROM point_info")
#     property_ids = [row[0] for row in cur.fetchall()]
#
#     cur.execute("SELECT command_id FROM command_info")
#     command_ids = [row[0] for row in cur.fetchall()]
#
#     # 生成raw_collected_data表数据
#     for _ in range(count):
#         time_stamp = random_timestamp()
#         property_id = random.choice(property_ids)
#         data_value = round(random.uniform(0, 100), 2)
#         created_at = random_timestamp()
#
#         cur.execute(
#             "INSERT INTO raw_collected_data (time_stamp, property_id, data_value, created_at) "
#             "VALUES (%s, %s, %s, %s)",
#             (time_stamp, property_id, data_value, created_at)
#         )
#
#     # 生成analysis_results表数据
#     for _ in range(count):
#         time_stamp = random_timestamp()
#         analysis_id = random.choice(analysis_ids)
#         analysis_value = round(random.uniform(0, 100), 2)
#         created_at = random_timestamp()
#
#         cur.execute(
#             "INSERT INTO analysis_results (time_stamp, analysis_id, analysis_value, created_at) "
#             "VALUES (%s, %s, %s, %s)",
#             (time_stamp, analysis_id, analysis_value, created_at)
#         )
#
#     # 生成command_data表数据
#     for _ in range(count):
#         time_stamp = random_timestamp()
#         command_id = random.choice(command_ids)
#         command_value = round(random.uniform(0, 100), 2)
#         created_at = random_timestamp()
#
#         cur.execute(
#             "INSERT INTO command_data (time_stamp, command_id, command_value, created_at) "
#             "VALUES (%s, %s, %s, %s)",
#             (time_stamp, command_id, command_value, created_at)
#         )
#
#     # 生成manual_parameters表数据
#     for _ in range(count):
#         time_stamp = random_timestamp()
#         supply_temp_upper = round(random.uniform(20, 30), 2)
#         return_temp_lower = round(random.uniform(10, 20), 2)
#         unit_flow = {
#             "type": random.choice(["水", "电", "气"]),
#             "value": round(random.uniform(1, 10), 2),
#             "unit": random.choice(["m³/h", "kW/h", "m³"])
#         }
#         cal_frequency = random.randint(1, 60)
#         valid_start = random_timestamp()
#         valid_end = valid_start + timedelta(days=random.randint(1, 30))
#         created_at = random_timestamp()
#         execution_mode = random.choice(["自动", "手动", "定时"])
#
#         # 使用 Json 适配器处理 JSONB 字段
#         cur.execute(
#             "INSERT INTO manual_parameters (time_stamp, supply_temp_upper, return_temp_lower, "
#             "unit_flow, cal_frequency, valid_start, valid_end, created_at, execution_mode) "
#             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#             (time_stamp, supply_temp_upper, return_temp_lower,
#              extras.Json(unit_flow), cal_frequency, valid_start, valid_end, created_at, execution_mode)
#         )
#
#     # 生成display_results表数据
#     for _ in range(count):
#         time_stamp = random_timestamp()
#         selected_points = [random.choice(property_ids) for _ in range(random.randint(1, 5))]
#         cal_method = random.choice(["平均值", "最大值", "最小值", "总和", "方差"])
#         created_at = random_timestamp()
#         calculated_value = round(random.uniform(0, 100), 2)
#
#         # 使用 Json 适配器处理 JSONB 字段
#         cur.execute(
#             "INSERT INTO display_results (time_stamp, selected_points, cal_method, created_at, calculated_value) "
#             "VALUES (%s, %s, %s, %s, %s)",
#             (time_stamp, extras.Json(selected_points), cal_method, created_at, calculated_value)
#         )
#
#     # 生成history_trend表数据
#     for _ in range(count):
#         timestamp = random_timestamp()
#         device_type = random.choice(["温湿度传感器", "电压传感器", "电流传感器", "功率计", "频率计"])
#         device_param = random.choice(["温度", "湿度", "电压", "电流", "功率", "频率"])
#         value = round(random.uniform(0, 100), 2)
#         calculation_method = random.choice(["原始值", "平均值", "最大值", "最小值"])
#
#         cur.execute(
#             "INSERT INTO history_trend (timestamp, device_type, device_param, value, calculation_method) "
#             "VALUES (%s, %s, %s, %s, %s)",
#             (timestamp, device_type, device_param, value, calculation_method)
#         )
#
#     # 生成yearly_analysis表数据
#     for _ in range(count):
#         time_stamp = random_date()
#         device_selection = f"设备组_{random.randint(1, 10)}"
#         parameter_selection = random.choice(["温度", "湿度", "电压", "电流", "功率", "频率"])
#         analysis_value = round(random.uniform(0, 100), 2)
#         created_at = random_timestamp()
#         unit = random.choice(["℃", "%", "V", "A", "kW", "Hz"])
#
#         cur.execute(
#             "INSERT INTO yearly_analysis (time_stamp, device_selection, parameter_selection, "
#             "analysis_value, created_at, unit) "
#             "VALUES (%s, %s, %s, %s, %s, %s)",
#             (time_stamp, device_selection, parameter_selection, analysis_value, created_at, unit)
#         )
#
#     # 生成hourly_analysis表数据
#     for _ in range(count):
#         time_stamp = random_timestamp()
#         device_selection = f"设备组_{random.randint(1, 10)}"
#         parameter_selection = random.choice(["温度", "湿度", "电压", "电流", "功率", "频率"])
#         analysis_value = round(random.uniform(0, 100), 2)
#         created_at = random_timestamp()
#         unit = random.choice(["℃", "%", "V", "A", "kW", "Hz"])
#
#         cur.execute(
#             "INSERT INTO hourly_analysis (time_stamp, device_selection, parameter_selection, "
#             "analysis_value, created_at, unit) "
#             "VALUES (%s, %s, %s, %s, %s, %s)",
#             (time_stamp, device_selection, parameter_selection, analysis_value, created_at, unit)
#         )
#
#     # 生成daily_analysis表数据
#     for _ in range(count):
#         time_stamp = random_date()
#         device_selection = f"设备组_{random.randint(1, 10)}"
#         parameter_selection = random.choice(["温度", "湿度", "电压", "电流", "功率", "频率"])
#         analysis_value = round(random.uniform(0, 100), 2)
#         created_at = random_timestamp()
#         unit = random.choice(["℃", "%", "V", "A", "kW", "Hz"])
#
#         cur.execute(
#             "INSERT INTO daily_analysis (time_stamp, device_selection, parameter_selection, "
#             "analysis_value, created_at, unit) "
#             "VALUES (%s, %s, %s, %s, %s, %s)",
#             (time_stamp, device_selection, parameter_selection, analysis_value, created_at, unit)
#         )
#
#     # 生成monthly_analysis表数据
#     for _ in range(count):
#         time_stamp = random_date()
#         device_selection = f"设备组_{random.randint(1, 10)}"
#         parameter_selection = random.choice(["温度", "湿度", "电压", "电流", "功率", "频率"])
#         analysis_value = round(random.uniform(0, 100), 2)
#         created_at = random_timestamp()
#         unit = random.choice(["℃", "%", "V", "A", "kW", "Hz"])
#
#         cur.execute(
#             "INSERT INTO monthly_analysis (time_stamp, device_selection, parameter_selection, "
#             "analysis_value, created_at, unit) "
#             "VALUES (%s, %s, %s, %s, %s, %s)",
#             (time_stamp, device_selection, parameter_selection, analysis_value, created_at, unit)
#         )
#
#
# # 执行数据生成
# try:
#     # truncate_tables()  # 取消注释以清空现有数据
#     generate_analysis_info(200)
#     generate_point_info(200)
#     generate_command_info(200)
#     generate_other_tables(200)
#     conn.commit()
#     print("数据生成成功！")
# except Exception as e:
#     conn.rollback()
#     print(f"数据生成失败: {e}")
# finally:
#     cur.close()
#     conn.close()
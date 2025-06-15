import psycopg2

# 创建数据库连接
conn = psycopg2.connect(
    database="xiangmingtest",
    user="postgres",
    password="000000",
    host="127.0.0.1",
    port="5432"
)

print('PostgreSQL数据库"xiangmingtest"连接成功!')

cursor = conn.cursor()

# 执行建表语句
cursor.execute('''
CREATE TABLE yearly_analysis (time_stamp date NOT NULL, device_selection character varying(64) NOT NULL, parameter_selection character varying(64) NOT NULL, analysis_value numeric NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP, unit character varying(50) NOT NULL);
CREATE TABLE analysis_results (time_stamp timestamp without time zone NOT NULL, analysis_id character varying(16) NOT NULL, analysis_value numeric NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE raw_collected_data (time_stamp timestamp without time zone NOT NULL, property_id character varying(16) NOT NULL, data_value numeric NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE manual_parameters (time_stamp timestamp without time zone NOT NULL, supply_temp_upper numeric, return_temp_lower numeric, unit_flow jsonb NOT NULL, cal_frequency integer, valid_start timestamp without time zone, valid_end timestamp without time zone, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP, execution_mode character varying(10) NOT NULL);
CREATE TABLE point_info (property_id character varying(16) NOT NULL, property_name character varying(64) NOT NULL, device_id character varying(16) NOT NULL DEFAULT NULL::character varying, device_name character varying(64) NOT NULL, category_name character varying(64) NOT NULL, area_name character varying(64) NOT NULL, value_unit character varying(16) NOT NULL, value_symbol character varying(16), status character varying(16) NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP, remark character varying(255));
CREATE TABLE display_results (time_stamp timestamp without time zone NOT NULL, selected_points jsonb NOT NULL, cal_method character varying(32) NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP, calculated_value numeric NOT NULL);
CREATE TABLE analysis_info (analysis_id character varying(16) NOT NULL, analysis_name character varying(64) NOT NULL, analysis_formula text, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE command_info (command_id character varying(16) NOT NULL, command_name character varying(64) NOT NULL, command_formula text, created_at timestamp without time zone, execution_mode character varying(10));
CREATE TABLE history_trend (timestamp timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, device_type character varying(50) NOT NULL, device_param character varying(50) NOT NULL, value numeric NOT NULL, calculation_method character varying(20) NOT NULL);
CREATE TABLE hourly_analysis (time_stamp timestamp without time zone NOT NULL, device_selection character varying(64) NOT NULL, parameter_selection character varying(64) NOT NULL, analysis_value numeric NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP, unit character varying(50) NOT NULL);
CREATE TABLE daily_analysis (time_stamp date NOT NULL, device_selection character varying(64) NOT NULL, parameter_selection character varying(64) NOT NULL, analysis_value numeric NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP, unit character varying(50) NOT NULL);
CREATE TABLE command_data (time_stamp timestamp without time zone NOT NULL, command_id character varying(16) NOT NULL, command_value numeric NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE monthly_analysis (time_stamp date NOT NULL, device_selection character varying(64) NOT NULL, parameter_selection character varying(64) NOT NULL, analysis_value numeric NOT NULL, created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP, unit character varying(50) NOT NULL);
CREATE TABLE model_input (
    time_stamp TIMESTAMP PRIMARY KEY,
    Qcooling numeric,
    Tin numeric,
    PIT numeric,
    Outdoor numeric,
    Tsupply numeric,
    Tset numeric
);
''')

conn.commit()  # 提交数据库事务

# 验证表创建结果
cursor.execute("""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name
""")
tables = cursor.fetchall()

print("\n数据库表列表：")
for table in tables:
    print(f"- {table[0]}")

# 检查索引创建情况
cursor.execute("""
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public'
  AND indexname LIKE 'idx_%'
""")
indexes = cursor.fetchall()

if indexes:
    print("\n创建的索引：")
    for idx in indexes:
        print(f"- {idx[0]} (表: {idx[1]})")

# 关闭连接
cursor.close()
conn.close()

print("\n数据库初始化完成！")
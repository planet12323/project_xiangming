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
-- 点位信息表
CREATE TABLE IF NOT EXISTS point_info (
    property_id VARCHAR(16) PRIMARY KEY NOT NULL, --主键，使用DCIM ID
    property_name VARCHAR(64) NOT NULL,
    device_id VARCHAR(16) NOT NULL,
    device_name VARCHAR(64) NOT NULL,
    category_name VARCHAR(64) NOT NULL,
    area_name VARCHAR(64) NOT NULL,
    value_unit VARCHAR(8) NOT NULL,
    value_symbol VARCHAR(16) NOT NULL,
    status VARCHAR(16) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 原始采集数据表
CREATE TABLE IF NOT EXISTS raw_collected_data (
    time_stamp TIMESTAMP NOT NULL,
    property_id VARCHAR(16) NOT NULL REFERENCES point_info(property_id),
    data_value NUMERIC(20,5) NOT NULL, -- 15位整数+5位小数
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (time_stamp, property_id)
);

-- 指令参数信息表
CREATE TABLE IF NOT EXISTS command_info (
    command_id VARCHAR(16) PRIMARY KEY NOT NULL,
    command_name VARCHAR(64) NOT NULL,
    command_formula TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 指令参数值表
CREATE TABLE IF NOT EXISTS command_data (
    time_stamp TIMESTAMP NOT NULL,
    command_id VARCHAR(16) NOT NULL REFERENCES command_info(command_id),
    command_value NUMERIC(20,5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (time_stamp, command_id)
);

-- 数据分析信息表
CREATE TABLE IF NOT EXISTS analysis_info (
    analysis_id VARCHAR(16) PRIMARY KEY NOT NULL,
    analysis_name VARCHAR(64) NOT NULL,
    analysis_formula TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 界面展示表
CREATE TABLE IF NOT EXISTS display_results (
    time_stamp TIMESTAMP PRIMARY KEY NOT NULL,
    selected_points JSONB NOT NULL,
    cal_method VARCHAR(32) NOT NULL, -- 熵值法/平均值法/最大值法
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 人工参数设定表
CREATE TABLE IF NOT EXISTS manual_parameters (
    time_stamp TIMESTAMP PRIMARY KEY NOT NULL,
    supply_temp_upper NUMERIC(10,2), -- 供水温度上限
    return_temp_lower NUMERIC(10,2), -- 回水温度下限
    unit_flow JSONB NOT NULL, -- 机组流量 {L-1:值, L-2:值, ...}
    cal_frequency INTEGER, -- 计算频率 单位:min
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 实时数据分析值表
CREATE TABLE IF NOT EXISTS analysis_results (
    time_stamp TIMESTAMP NOT NULL,
    analysis_id VARCHAR(16) NOT NULL REFERENCES analysis_info(analysis_id),
    analysis_value NUMERIC(20,5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (time_stamp, analysis_id)
);

-- 小时分析表，每小时更新一次
CREATE TABLE IF NOT EXISTS hourly_analysis (
    time_stamp TIMESTAMP PRIMARY KEY NOT NULL,
    device_selection VARCHAR(64) NOT NULL, -- 设备选择
    parameter_selection VARCHAR(64) NOT NULL, -- 参数选择
    analysis_value NUMERIC(20,5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 日分析表，每日更新
CREATE TABLE IF NOT EXISTS daily_analysis (
    time_stamp TIMESTAMP PRIMARY KEY NOT NULL,
    device_selection VARCHAR(64) NOT NULL, -- 选择的设备
    parameter_selection VARCHAR(64) NOT NULL, -- 选择的参数
    analysis_value NUMERIC(20,5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 月分析表，每月更新
CREATE TABLE IF NOT EXISTS monthly_analysis (
    time_stamp TIMESTAMP PRIMARY KEY NOT NULL,
    device_selection VARCHAR(64) NOT NULL,
    parameter_selection VARCHAR(64) NOT NULL,
    analysis_value NUMERIC(20,5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 年分析表
CREATE TABLE IF NOT EXISTS yearly_analysis (
    time_stamp TIMESTAMP PRIMARY KEY NOT NULL,
    device_selection VARCHAR(64) NOT NULL,
    parameter_selection VARCHAR(64) NOT NULL,
    analysis_value NUMERIC(20,5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_rcd_timestamp ON raw_collected_data (time_stamp DESC);
CREATE INDEX IF NOT EXISTS idx_cpd_timestamp ON command_data (time_stamp DESC);
CREATE INDEX IF NOT EXISTS idx_ar_timestamp ON analysis_results (time_stamp DESC);
CREATE INDEX IF NOT EXISTS idx_display_timestamp ON display_results (time_stamp DESC);
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
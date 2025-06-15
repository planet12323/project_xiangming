import numpy as np
import pandas as pd
import re
from datetime import datetime

# ================================================================
# 配置参数（无需预知数据规模）
# ================================================================
input_path = r"C:\Users\86130\Desktop\CHenziyi1\6.5.csv"
output_path = f"温度统计报表_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

# 列定义（根据常见需求设定，可修改）
timestamp_col = 0       # 时间戳列位置（第1列）
data_start_col = 5       # 数据起始列（F列=索引5）

# ================================================================
# 核心处理函数
# ================================================================
def preprocess_value(value):
    """智能数据清洗：转换特殊值并过滤零/空值，同时过滤18-27度范围外的值"""
    try:
        # 处理空值和特殊标记
        str_val = str(value).strip()
        if not str_val or str_val.lower() in ['nan', 'null', 'q', 'n=1']:
            return np.nan
        
        # 处理分数格式（支持$\frac{25}{1}$和25/1）
        if '/' in str_val:
            nums = re.findall(r'\d+', str_val)
            if len(nums) >= 2:
                num = float(nums[0]) / float(nums[1])
                # 新增：过滤18-27度范围外的值
                return num if 18 <= num <= 27 else np.nan
            return np.nan
        
        # 数值转换与零值过滤
        num = float(str_val)
        # 新增：过滤18-27度范围外的值
        if num != 0 and 18 <= num <= 27:
            return num
        return np.nan
    except:
        return np.nan

def calculate_global_weights(data_matrix):
    """全局熵权计算（自动处理缺失值）"""
    # 数据有效性检查
    valid_matrix = data_matrix[~np.isnan(data_matrix).all(axis=1)]
    if valid_matrix.size == 0 or valid_matrix.shape[0] < 2:
        return None
    
    # 标准化处理（忽略NaN）
    with np.errstate(divide='ignore', invalid='ignore'):
        X = valid_matrix / np.nansum(valid_matrix, axis=0)
    X = np.where((X > 0) & ~np.isnan(X), X, 1e-12)  # 避免零和NaN
    
    # 熵值计算
    log_X = np.log(X)
    e = -np.nansum(X * log_X, axis=0) / np.log(X.shape[0])
    d = 1 - e
    return d / np.nansum(d)

# ================================================================
# 主处理流程
# ================================================================
# 读取完整数据（自动检测行列）
# 修改后的读取方式
raw_df = pd.read_csv(
    input_path,
    header=None,
    dtype=str,
    encoding='gbk',  # 改用GBK编码
    engine='python'  # 指定解析引擎
)

# 动态确定数据列范围
data_cols = list(range(data_start_col, raw_df.shape[1]))

# 数据预处理（并行加速）
data_matrix = np.vectorize(preprocess_value)(raw_df.iloc[1:, data_cols].to_numpy())

# 计算全局权重
global_weights = calculate_global_weights(data_matrix.astype(float))

# 逐行生成统计结果
results = []
for i in range(data_matrix.shape[0]):
    # 时间戳解析
    ts_str = str(raw_df.iloc[i+1, timestamp_col])  # +1跳过标题行
    ts_clean = re.sub(r'[^0-9-]', '', ts_str)[:8]   # 提取类似"07-04-18"
    ts_formatted = f"{ts_clean[:2]}-{ts_clean[2:4]}-{ts_clean[4:6]}" if len(ts_clean)>=6 else "时间无效"
    
    # 当前行有效数据
    row_data = data_matrix[i].astype(float)
    valid_mask = ~np.isnan(row_data)
    valid_values = row_data[valid_mask]
    
    # 统计量计算
    stats = {
        '时间': ts_formatted,
        '均值': np.nan if len(valid_values)==0 else round(np.mean(valid_values), 2),
        '最大值': np.nan if len(valid_values)==0 else round(np.max(valid_values), 2),
        '特征温度': np.nan
    }
    
    # 动态特征温度计算
    if global_weights is not None and valid_mask.any():
        active_weights = global_weights[valid_mask]
        active_weights /= active_weights.sum()  # 重新归一化
        stats['特征温度'] = round(np.dot(valid_values, active_weights), 2)
    
    results.append(stats)

# ================================================================
# 输出报表（自适应布局）
# ================================================================
output_df = pd.DataFrame(results)
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    # 统计表
    output_df.to_excel(
        writer,
        sheet_name='温度统计',
        index=False,
        header=['时间', '平均温度', '峰值温度', '熵权特征温度'],
        startrow=1
    )
    
    # 添加标题
    workbook = writer.book
    worksheet = writer.sheets['温度统计']
    header_format = workbook.add_format({
        'bold': True, 
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 14
    })
    worksheet.merge_range('A1:D1', '设备温度统计报表', header_format)
    
    # 列宽自适应
    worksheet.set_column('A:A', 14)  # 时间列
    worksheet.set_column('B:C', 12)  # 温度值
    worksheet.set_column('D:D', 16)  # 特征温度

print(f"报表生成成功: {output_path}")

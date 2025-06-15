from http_services import helper_http
from sql_services.sql_helper import *
import time
from config import *
from http_services import *
import http_services.helper_http
import json
from decimal import Decimal
import numpy as np
import IDC


def fetch_settings() -> Config:
    seleted_points, cal_method = get_display_results()  #
    static_symbol, Tin = get_static_symbol()
    supply_temp_upper, return_temp_lower, unit_flow, cal_frequency = get_manual_parameters()[0]
    conf = Config(Tin=seleted_points, static_symbol_lists=static_symbol, cal_method=cal_method, supply_temp_upper=supply_temp_upper,
                  return_temp_lower=return_temp_lower, unit_flow=unit_flow, cal_frequency=cal_frequency)
    return conf


def fetch_data(url, selected_points, timestamp):
    static_points = list(get_point_info_except_Tin())
    property_ids = static_points + selected_points
    data = helper_http.get_real_time_data(url, property_ids=property_ids) #  data: list<dict>
    data = json.dumps(data).encode('raw_unicode_escape').decode('utf-8')[0]
    data = json.loads(data)['Data']
    raw_data_triple = [(timestamp, pid, next((Decimal(item["curvalue"]) for item in data if item["property_id"] == pid), "N/A"))
              for pid in property_ids]
    data_dict = {item["property_id"]: Decimal(item["curvalue"]) for item in data}
    raw_data_dict = {pid: data_dict.get(pid, "N/A") for pid in property_ids}
    return raw_data_triple, raw_data_dict


def data_process_by_method(raw_data_dict, configs):
    vars = dict()
    vars_sum = list(configs.static_symbol_lists.keys())
    for v in vars_sum:
        pid_lst = configs.static_symbol_lists[v]
        for pid in pid_lst:
            if raw_data_dict.get(pid) == "N/A":
                vars[v] += 0
                continue
            vars[v] += raw_data_dict.get(pid)

    vars['Qcooling'] = (4.2 * vars['V_1'] * (vars['Treturn_1'] - vars['Tsupply_1'] / 3.6) +
                        4.2 * vars['V_2'] * (vars['Treturn_2'] - vars['Tsupply_2'] / 3.6))

    vars['Tsupply'] = (vars['Tsupply_1'] + vars['Tsupply_2']) / 2

    temps = []
    for ti in configs.Tin:
        if raw_data_dict.get(ti) == "N/A": continue
        temps.append(raw_data_dict.get(ti))
    vars['Tin'] = {'平均值法':np.mean(temps),
                   '最大值法':np.max(temps),
                   '熵值法':calculate_feature_temperature(np.array(temps).reshape(1,len(temps)))}
    vars['Tset'] = 22
    return vars

def calculate_feature_temperature(X):
    # 确保输入是二维数组且n = 1
    if X.shape[0] != 1:
        raise ValueError("n must be 1 for this implementation")

    n, m = X.shape
    # 第一步：计算温度比重
    p = np.zeros(m)
    sum_x = np.sum(X)
    for j in range(m):
        p[j] = X[0][j] / sum_x

    # 第二步：计算熵值(由于n = 1，这里e_j恒为0，因为ln(p_ij)中p_ij只有一个值且sum(p_ij)=1，此时p_ij = 1，ln(1)=0)
    e = 0

    # 第三步：计算信息熵冗余
    d = 1 - e

    # 第四步：计算权重
    w = d / np.sum(d)

    # 第五步：计算特征温度
    T = np.sum(w * X[0])
    return T


def raw_data_analysis(raw_data_dict, W, Tin):
    ana_res = {
        'Qcooling#1': 4.2 * raw_data_dict['G1'] * (raw_data_dict['tei_1'] - raw_data_dict['teo_1']) / 3.6,
        'Qcooling#2': 4.2 * raw_data_dict['G2'] * (raw_data_dict['tei_2'] - raw_data_dict['teo_2']) / 3.6,
        'Qcooling#3': 4.2 * raw_data_dict['G3'] * (raw_data_dict['tei_3'] - raw_data_dict['teo_3']) / 3.6,
        'Qcooling#4': 4.2 * raw_data_dict['G4'] * (raw_data_dict['tei_4'] - raw_data_dict['teo_4']) / 3.6,
        'W_1’': raw_data_dict['W_1'] - W[0][1],
        'W_2’': raw_data_dict['W_2'] - W[1][1],
        'W_3’': raw_data_dict['W_3'] - W[2][1],
        'W_4’': raw_data_dict['W_4'] - W[3][1],
        'PLR1': (4.2 * raw_data_dict['G1'] * (raw_data_dict['tei_1'] - raw_data_dict['teo_1']) / 3.6) / 350,
        'PLR2': (4.2 * raw_data_dict['G2'] * (raw_data_dict['tei_2'] - raw_data_dict['teo_2']) / 3.6) / 350,
        'PLR3': (4.2 * raw_data_dict['G3'] * (raw_data_dict['tei_3'] - raw_data_dict['teo_3']) / 3.6) / 886,
        'PLR4': (4.2 * raw_data_dict['G4'] * (raw_data_dict['tei_4'] - raw_data_dict['teo_4']) / 3.6) / 886,
        'COP#1': (4.2 * raw_data_dict['G1'] * (raw_data_dict['tei_1'] - raw_data_dict['teo_1']) / 3.6) / raw_data_dict[
            'Pc_1'],
        'COP#2': (4.2 * raw_data_dict['G2'] * (raw_data_dict['tei_2'] - raw_data_dict['teo_2']) / 3.6) / raw_data_dict[
            'Pc_2'],
        'COP#3': (4.2 * raw_data_dict['G3'] * (raw_data_dict['tei_3'] - raw_data_dict['teo_3']) / 3.6) / raw_data_dict[
            'Pc_3'],
        'COP#4': (4.2 * raw_data_dict['G4'] * (raw_data_dict['tei_4'] - raw_data_dict['teo_4']) / 3.6) / raw_data_dict[
            'Pc_4'],
        'W': (raw_data_dict['W_1'] - W[0][1]) + (raw_data_dict['W_2'] - W[1][1]) + (raw_data_dict['W_3'] - W[2][1]) + (
                    raw_data_dict['W_4'] - W[3][1]),
        'SCOP': sum(
            4.2 * raw_data_dict[f'G{i}'] * (raw_data_dict[f'tei_{i}'] - raw_data_dict[f'teo_{i}']) / 3.6 for i in
            range(1, 5)) / sum(raw_data_dict[f'Pc_{i}'] for i in range(1, 5)),
        'Tin': Tin
    }
    return ana_res



if __name__ == '__main__':
    while True:
        timestamp = time.time()
        configs = fetch_settings() #  read from database

        #  raw_data_triple(timestamp, pid, value), raw_data_dict{'symbol':pid}
        raw_data_triple, raw_data_dict = fetch_data(configs.url_GetRealTimeData,configs.Tin, timestamp) #  get from http

        W = get_W()
        update_raw_collected_data(raw_data_triple) #  update database

        input_variables = data_process_by_method(raw_data_dict, configs)
        input_tuple = (timestamp, input_variables['Qcooling'],input_variables['Tin'][configs.cal_method],input_variables['PIT'],
                       input_variables['Outdoor'], input_variables['Tsupply'], input_variables['Tset'])
        update_model_input(input_tuple)


        ana_res = raw_data_analysis(raw_data_dict, W, input_variables['Tin'][configs.cal_method])
        aids = list(ana_res.keys())
        data = [(timestamp, aid, ana_res[aid]) for aid in aids]
        update_analysis_results(data)
        update_hourly_analysis(timestamp)
        update_daily_analysis(timestamp)
        update_monthly_analysis(timestamp)
        update_yearly_analysis(timestamp)
        
        cur_inputs = get_model_input(IDC.step*2 + IDC.rows_to_predict) #  step * [qcooling, tin, pit, outdoor, tsupply, tset]
        cur_inputs = np.array(cur_inputs)[:, 1:].astype(float)  # qcooling, tin, pit, outdoor, tsupply, tset
        n, m = cur_inputs.shape
        data1 = np.hstack((cur_inputs[:n - 1, 0:4], cur_inputs[1:n, 4:5]))
        data2 = np.hstack((cur_inputs[:n - 1, 0:2], cur_inputs[:n - 1, 4:5],
                           cur_inputs[:n - 1, 2:4], cur_inputs[1:n, 0:1],
                           cur_inputs[:n - 1, m - 1:m]))
        data3 = cur_inputs[:n - 1, 3:4]
        result = IDC.main_idc(data1, data2, data3)

        commands = {"flow_l1": result['Vmaglev1'],
                      "flow_l2": result['Vmaglev2'],
                      "flow_l3": result['Vscrew1'],
                      "flow_l4": result['Vscrew2'],
                      "supply_temp": result['Supply'],
                      "temperature_difference": result['DeltaT']
                    }
        helper_http.send_command(configs.url_frontend, commands)
        time.sleep(configs.cal_frequency * 60)

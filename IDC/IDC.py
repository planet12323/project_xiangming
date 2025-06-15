import pandas as pd
import numpy as np
from pyswarm import pso
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from typing import Dict

# 数据归一化处理


# 参数
batchsize = 1  # 批处理大小，预测模型里是32
step = 5  # 时间步数
loaddim = 5  # 负荷预测模型输入维度
tempdim = 6  # 温度预测模型输入维度
rows_to_predict = 3  # 进行预测的迭代次数，序列长度为step，步长为1
nextTin = 0  # 中间变量Tin(t+1)，具体数值不重要
Beta = 0.000008  # 可变参数β
Alpha = 1 - Beta  # 可变参数α

T_max, T_min = 22.89888889, 22.69222222  # Tin训练集 max=22.89888889，min=22.69222222
C_max, C_min = 1193.96, 1153.82  # Cooling训练集 max=1193.96，min=1153.82
nextTset = 23

# 加载负荷预测模型
loadmodel = tf.keras.models.load_model('1117_loadpred.keras')
# 加载温度预测模型
tempmodel = tf.keras.models.load_model('1117_temppred.keras')


################## 热泵能耗方程：##################
# 1号热泵：磁悬浮1
def PphCal1(Cooling1, nextTreturn, nextTout):
    return Cooling1 / (0.114064992 * Cooling1
                       + 9.86011205 * nextTreturn
                       - 0.394321578 * nextTout
                       + 0.0000450464015 * Cooling1 * Cooling1
                       - 0.00581368122 * Cooling1 * nextTreturn
                       - 0.000758651811 * Cooling1 * nextTout
                       - 0.326362421 * nextTreturn * nextTreturn
                       + 0.0184361005 * nextTreturn * nextTout
                       + 0.00239640342 * nextTout * nextTout - 71.6350077532962)


# 2号热泵：磁悬浮2
def PphCal2(Cooling2, nextTreturn, nextTout):
    return Cooling2 / (- 0.031207272 * Cooling2
                       - 5.57093763 * nextTreturn
                       - 0.178609075 * nextTout
                       - 0.000140286197 * Cooling2 * Cooling2
                       + 0.0081496977 * Cooling2 * nextTreturn
                       - 0.000599404697 * Cooling2 * nextTout
                       + 0.150016223 * nextTreturn * nextTreturn
                       - 0.00555278723 * nextTreturn * nextTout
                       + 0.00426582024 * nextTout * nextTout + 48.815621285422)


# 3号热泵：螺杆1
def PphCal3(Cooling3, nextTreturn, nextTout):
    return Cooling3 / (- 0.0565696352 * Cooling3
                       + 140.258199 * nextTreturn
                       + 0.297813736 * nextTout
                       - 0.000000512788461 * Cooling3 * Cooling3
                       + 0.00512409975 * Cooling3 * nextTreturn
                       - 0.000396810401 * Cooling3 * nextTout
                       - 5.00822474 * nextTreturn * nextTreturn
                       - 0.00851263147 * nextTreturn * nextTout
                       - 0.000209590663 * nextTout * nextTout - 986.272338515734)


# 4号热泵：螺杆2
def PphCal4(Cooling4, nextTreturn, nextTout):
    return Cooling4 / (- 0.0316576759 * Cooling4
                       - 9.98926426 * nextTreturn
                       + 0.0902543953 * nextTout
                       + 0.0000000479863189 * Cooling4 * Cooling4
                       + 0.00257982592 * Cooling4 * nextTreturn
                       - 0.0000778893844 * Cooling4 * nextTout
                       + 0.295875914 * nextTreturn * nextTreturn
                       - 0.00932111852 * nextTreturn * nextTout
                       + 0.000430676823 * nextTout * nextTout + 84.2195052674394)


# 测试热泵模型
# print("热泵模型测试结果:")
# power1 = PphCal1(173.34, 14.55, 37.91)
# print("磁悬浮1功率:", power1)
# power2 = PphCal2(191.78, 14.59, 37.91)
# print("磁悬浮2功率:", power2)
# power3 = PphCal3(646.4, 14.31, 37.91)
# print("螺杆1功率:", power3)
# power4 = PphCal4(587.45, 14.58, 37.91)
# print("螺杆2功率:", power4)


################## 水泵能耗方程：##################
def PwpCal(Volume):
    return 0.0238 * Volume * Volume - 5.27 * Volume + 306.7


# 测试水泵模型
print("\n水泵模型测试结果:")
pump = PwpCal(120)
print("水泵功率:", pump)


################## 负荷能量守恒方程：##################
def Constraint1(x, Cooling):
    nextTsupply, deltaT, nextVscrew1, nextVscrew2, nextVmaglev1, nextVmaglev2 = x
    nextTreturn = nextTsupply + deltaT  # 通过供回水温差计算回水温度
    total_volume = nextVscrew1 + nextVscrew2 + nextVmaglev1 + nextVmaglev2
    return (Cooling == deltaT * total_volume * 4.2 / 3.6) and nextTsupply < nextTreturn


################## 代价函数：##################
def Cost(x, Alpha, Beta, nextTset, nextTout, Cooling, tempdata):
    nextTsupply, deltaT, nextVscrew1, nextVscrew2, nextVmaglev1, nextVmaglev2 = x
    nextTreturn = nextTsupply + deltaT
    total_volume = nextVscrew1 + nextVscrew2 + nextVmaglev1 + nextVmaglev2

    # 水泵流量 = 总流量 / 3
    volume_pump = total_volume / 3
    Pwp = PwpCal(volume_pump)

    # 按流量比例分配冷量
    total_flow = total_volume
    Cooling_screw1 = Cooling * (nextVscrew1 / total_flow)
    Cooling_screw2 = Cooling * (nextVscrew2 / total_flow)
    Cooling_maglev1 = Cooling * (nextVmaglev1 / total_flow)
    Cooling_maglev2 = Cooling * (nextVmaglev2 / total_flow)

    Php1 = PphCal1(Cooling_maglev1, nextTreturn, nextTout)
    Php2 = PphCal2(Cooling_maglev2, nextTreturn, nextTout)
    Php3 = PphCal3(Cooling_screw1, nextTreturn, nextTout)
    Php4 = PphCal4(Cooling_screw2, nextTreturn, nextTout)

    # 温度预测部分
    if tempdata.shape != (step, tempdim):
        tempdata = tempdata.reshape((step, tempdim))

    tempdata_modified = tempdata.copy()
    tempdata_modified[-1, 5] = nextTsupply
    tempinput = tempdata_modified.reshape((batchsize, step, tempdim))

    global nextTin
    global nextTin_scaled
    nextTin_scaled = tempmodel.predict(tempinput, verbose=0)[0][0]
    nextTin = nextTin_scaled * (T_max - T_min) + T_min

    # 添加功率非负约束
    if any(p < 0 for p in [Php1, Php2, Php3, Php4]):
        return float('inf')  # 返回极大值表示无效解

    cost = Alpha * (nextTset - nextTin) ** 2 + Beta * (Php1 + Php2 + Php3 + Php4 + Pwp * 3) ** 2
    return cost


def main_idc(data1, data2, data3) -> Dict:
    print("\n开始主优化程序...")
    x = []
    cf = []
    co = []
    tin = []
    sc1 = []
    ma1 = []
    sc2 = []
    ma2 = []
    pu = []
    tot = []
    deltaT_list = []  # 存储供回水温差
    scaler = MinMaxScaler()
    data1_scaled = scaler.fit_transform(data1)
    data2_scaled = scaler.fit_transform(data2)
    for i in range(rows_to_predict):
        print('滚动次数：', i)
        # 获取温度预测输入数据 (5个时间步，每个时间步7个特征)
        tempdata = data2_scaled[i:i + step, 0:tempdim]  # 形状应为(5,7)

        # 获取负荷预测输入数据
        loaddata = data1_scaled[i:i + step, 0:loaddim]
        loadinput = loaddata.reshape((batchsize, step, loaddim))

        Cooling_scaled = loadmodel.predict(loadinput, verbose=0)[0][0]
        Cooling = Cooling_scaled * (C_max - C_min) + C_min
        nextTout = data3[i + 5, 0]

        # 优化变量上下界：供温、温差、螺杆1流量、螺杆2流量、磁悬浮1流量、磁悬浮2流量
        lb = [11, 3.5, 120, 120, 35, 35]
        ub = [12, 4.5, 160, 160, 110, 110]

        Constraint_with_param = lambda x: Constraint1(x, Cooling)
        Cost_with_param = lambda x: Cost(x, Alpha, Beta, nextTset, nextTout, Cooling, tempdata)
        xopt, fopt = pso(Cost_with_param, lb, ub, f_ieqcons=Constraint_with_param, minfunc=0.1, maxiter=50)

        # 更新数据用于下一次预测
        data2_scaled[i + 5, 1] = Cooling_scaled * 0.6 + data2_scaled[i + 5, 1] * 0.4
        data2_scaled[i + 6, 6] = Cooling_scaled * 0.6 + data2_scaled[i + 6, 6] * 0.4
        data1_scaled[i + 5, 0] = Cooling_scaled * 0.6 + data1_scaled[i + 5, 0] * 0.4
        data1_scaled[i + 5, 1] = nextTin_scaled * 0.4 + data1_scaled[i + 5, 1] * 0.6
        data2_scaled[i + 5, 2] = nextTin_scaled * 0.4 + data2_scaled[i + 5, 2] * 0.6

        # 从优化结果中提取变量
        nextTsupply, deltaT, nextVscrew1, nextVscrew2, nextVmaglev1, nextVmaglev2 = xopt
        nextTreturn = nextTsupply + deltaT
        total_volume = nextVscrew1 + nextVscrew2 + nextVmaglev1 + nextVmaglev2

        # 计算冷量分配
        volume_pump = total_volume / 3
        Cooling_screw1 = Cooling * nextVscrew1 / total_volume
        Cooling_screw2 = Cooling * nextVscrew2 / total_volume
        Cooling_maglev1 = Cooling * nextVmaglev1 / total_volume
        Cooling_maglev2 = Cooling * nextVmaglev2 / total_volume

        # 计算功率
        power_screw1 = PphCal3(Cooling_screw1, nextTreturn, nextTout)
        power_screw2 = PphCal4(Cooling_screw2, nextTreturn, nextTout)
        power_maglev1 = PphCal1(Cooling_maglev1, nextTreturn, nextTout)
        power_maglev2 = PphCal2(Cooling_maglev2, nextTreturn, nextTout)
        power_pump = PwpCal(volume_pump)
        power_total = (power_screw1 + power_maglev1 + power_screw2 + power_maglev2) + 3 * power_pump
        # 存储结果
        deltaT_list.append(deltaT)
        print('供温，温差，螺杆1流量，螺杆2流量，磁悬浮1流量，磁悬浮2流量:', xopt)
        print('供回水温差:', deltaT)
        print('Cost:', fopt)
        print('总冷量：', Cooling)
        print('室温：', nextTin)
        print('螺杆1功率：', power_screw1)
        print('螺杆2功率：', power_screw2)
        print('磁悬浮1功率：', power_maglev1)
        print('磁悬浮2功率：', power_maglev2)
        print('水泵功率：', power_pump)
        print('总功率：', power_total)

        x.append(xopt)
        cf.append(fopt)
        co.append(Cooling)
        tin.append(nextTin)
        sc1.append(power_screw1)
        sc2.append(power_screw2)
        ma1.append(power_maglev1)
        ma2.append(power_maglev2)
        pu.append(power_pump)
        tot.append(power_total)
        deltaT_list.append(deltaT)

    print('最终优化结果：')
    print('优化变量[供温, 温差, 螺杆1流量, 螺杆2流量, 磁悬浮1流量, 磁悬浮2流量]:', x)
    print('代价函数最优值：', cf)
    print('冷量变化：', co)
    print('室温：', tin)
    print('供回水温差变化：', deltaT_list)

    # 提取结果中的各个变量
    supply_temp = [arr[0] for arr in x]
    deltaT = [arr[1] for arr in x]
    screw1_flow = [arr[2] for arr in x]
    screw2_flow = [arr[3] for arr in x]
    maglev1_flow = [arr[4] for arr in x]
    maglev2_flow = [arr[5] for arr in x]

    result = {
        'Supply': np.mean(supply_temp),
        'DeltaT': np.mean(deltaT),
        'Vscrew1': np.mean(screw1_flow),
        'Vscrew2': np.mean(screw2_flow),
        'Vmaglev1': np.mean(maglev1_flow),
        'Vmaglev2': np.mean(maglev2_flow),
        'Cooling': co,
        'Temp': tin,
        'Pscrew1': sc1,
        'Pscrew2': sc2,
        'Pmaglev1': ma1,
        'Pmaglev2': ma2,
        'Ppump': pu,
        'Total_power': tot
    }
    return result
    # re = pd.DataFrame(result)
    # print(re)
    # re.to_csv('optimization_output.csv', index=False)


if __name__ == '__main__':
    # 读取Excel文件
    excel_file1 = "1117_load.xls"  # 负荷预测输入数据集
    excel_file2 = "1117_temp.xls"  # 温度预测输入数据集，设定温度也在这里面
    excel_file3 = "1117_weather.xls"  # 气象预报输入数据集
    data1 = pd.read_excel(excel_file1, usecols="A:E", header=None)  # batch * [Qcooling, Tin, PIT, Outdoor, Outdoor_t-1]
    data2 = pd.read_excel(excel_file2, usecols="A:G",
                          header=None)  # batch * [ Qcooling, Tin, Tsupply, PIT, Outdoor, Qcooling_t-1, Tset]
    data3 = np.array(pd.read_excel(excel_file3, usecols="A", header=None))  # batch * [Outdoor]
    print(data1.shape)
    print(data2.shape)
    print(data3.shape)
    result = main_idc(data1, data2, data3)
    print(result)
    print('j')

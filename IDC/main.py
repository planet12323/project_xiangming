from sql_services.sql_helper import *
from http_services.json_helper import *
import time
from config import *


def fetch_settings() -> Config:
    seleted_points, cal_method = get_points_calmethod()  #
    supply_temp_upper, return_temp_lower, unit_flow, cal_frequency = get_manual_parameters()[0]
    conf = Config(selected_points=seleted_points, cal_method=cal_method, supply_temp_upper=supply_temp_upper,
                  return_temp_lower=return_temp_lower, unit_flow=unit_flow, cal_frequency=cal_frequency)
    return conf


if __name__ == '__main__':
    while True:
        configs = fetch_settings()
        fetch_data(configs.selected_points)
        data_process()
        write_database()
        main_IDC()
        result_analysis()
        analysis_write_database()
        send_command()
        time.sleep(configs.cal_frequency * 60)

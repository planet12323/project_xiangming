from typing import List, Dict, Optional, Any

class Config:
    """系统配置类，用于存储和管理系统参数"""

    def __init__(
            self,
            Tin: Optional[List[str]] = None,
            static_symbol_lists: Optional[Dict] = None,
            cal_method: str = "max",
            supply_temp_upper: float = 40.0,
            return_temp_lower: float = 20.0,
            unit_flow: Optional[Dict[str, Any]] = None,
            cal_frequency: int = 30
    ):
        self.Tin = Tin or [ "R5S01001", "R5S01004", "R5S02001", "R5S02004", "R5S03001",
                    "R5S03004", "R5S04001", "R5S04004", "R5S05001", "R5S05004", "R5S06001",
                    "R5S06004", "R5S07001", "R5S07004", "R5S08001", "R5S08004", "R5S09001",
                    "R5S09004", "R5S10001", "R5S10004", "R5S11001", "R5S11004", "R5S12001",
                    "R5S12004", "JC701001", "JC701004", "JC702001", "JC702004", "JC703001",
                    "JC703004", "JC704001", "JC704004", "JC705001", "JC705004", "JC706001",
                    "JC706004", "JC707001", "JC707004", "JC708001", "JC708004", "JC709001",
                    "JC709004", "JC710001", "JC710004", "JC711001", "JC711004", "JC712001",
                    "JC712004", "T7F07003", "T7F06003", "T7F05003", "T7F04003", "HJ030001",
                    "HJ024001", "HJ024003", "T7F07001", "T7F06001", "T7F05001", "T7F04001",
                    "HJ030003", "HJ024005", "HJ024007", "T7F13003", "T7F12003", "T7F11003",
                    "T7F10003", "T7F09003", "T7F08003", "T7F13001", "T7F12001", "T7F11001",
                    "T7F10001", "T7F09001", "T7F08001", "HJ025001", "HJ025003", "HJ025005",
                    "HJ025007", "HJ025009", "HJ025011", "HJ025013", "HJ025015", "HJ025017",
                    "HJ025019", "HJ025021", "HJ025023", "JC713001", "JC713004", "JC714001",
                    "JC714004", "JC715001", "JC715004", "R5S13001", "R5S13004", "R5S14001",
                    "R5S14004", "R5S15001", "R5S15004", "T7F01003", "T7F01001", "T7F02003",
                    "T7F02001", "T7F03003", "T7F03001", "T7F15003", "T7F15001", "T7F14003",
                    "T7F14001", "HJ006001", "HJ006003", "HJ006005", "HJ006007"]
        self.cal_method = cal_method
        self.supply_temp_upper = supply_temp_upper
        self.return_temp_lower = return_temp_lower
        self.unit_flow = unit_flow or {}
        self.cal_frequency = cal_frequency
        self.url_GetDeviceList = 'http://192.168.1.246:10088/api/GetDeviceList'
        self.url_GetRealTimeData = 'http://192.168.1.246:10088/api/GetRealTimeData'
        self.url_frontend = 'https://139.129.89.24/niagara/xm/tms/device/setControlPoints'
        self.static_symbol_lists = static_symbol_lists


    def to_dict(self) -> Dict[str, Any]:
        """将配置对象转换为字典"""
        return {
            'Tin': self.Tin,
            'cal_method': self.cal_method,
            'supply_temp_upper': self.supply_temp_upper,
            'return_temp_lower': self.return_temp_lower,
            'unit_flow': self.unit_flow,
            'cal_frequency': self.cal_frequency
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """从字典创建配置对象"""
        return cls(
            Tin=config_dict.get('Tin', []),
            cal_method=config_dict.get('cal_method', 'max'),
            supply_temp_upper=config_dict.get('supply_temp_upper', 40.0),
            return_temp_lower=config_dict.get('return_temp_lower', 20.0),
            unit_flow=config_dict.get('unit_flow', {}),
            cal_frequency=config_dict.get('cal_frequency', 30)
        )

    def validate(self) -> bool:
        """验证配置参数的有效性"""
        # 验证计算方法
        if self.cal_method not in ['max', 'min', 'avg']:
            return False

        # 验证温度范围
        if self.supply_temp_upper <= self.return_temp_lower:
            return False

        # 验证计算频率
        if self.cal_frequency <= 0:
            return False

        return True

    def __str__(self) -> str:
        """配置对象的字符串表示"""
        return (
            f"Config(Tin={len(self.Tin)} items, "
            f"cal_method={self.cal_method}, "
            f"supply_temp_upper={self.supply_temp_upper}, "
            f"return_temp_lower={self.return_temp_lower}, "
            f"unit_flow={len(self.unit_flow)} items, "
            f"cal_frequency={self.cal_frequency} min)"
        )



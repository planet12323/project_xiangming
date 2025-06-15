from typing import List, Dict, Optional, Any

class Config:
    """系统配置类，用于存储和管理系统参数"""

    def __init__(
            self,
            selected_points: Optional[List[str]] = None,
            cal_method: str = "max",
            supply_temp_upper: float = 40.0,
            return_temp_lower: float = 20.0,
            unit_flow: Optional[Dict[str, Any]] = None,
            cal_frequency: int = 30
    ):
        """
        初始化配置对象

        Args:
            selected_points: 选中的点位列表
            cal_method: 计算方法（max/min/avg）
            supply_temp_upper: 供水温度上限
            return_temp_lower: 回水温度下限
            unit_flow: 机组流量配置
            cal_frequency: 计算频率（分钟）
        """
        self.selected_points = selected_points or []
        self.cal_method = cal_method
        self.supply_temp_upper = supply_temp_upper
        self.return_temp_lower = return_temp_lower
        self.unit_flow = unit_flow or {}
        self.cal_frequency = cal_frequency
        self.GetDeviceList = 'http://192.168.1.246:10088/api/GetDeviceList'
        self.GetRealTimeData = 'http://192.168.1.246:10088/api/GetRealTimeData'


    def to_dict(self) -> Dict[str, Any]:
        """将配置对象转换为字典"""
        return {
            'selected_points': self.selected_points,
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
            selected_points=config_dict.get('selected_points', []),
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
            f"Config(selected_points={len(self.selected_points)} items, "
            f"cal_method={self.cal_method}, "
            f"supply_temp_upper={self.supply_temp_upper}, "
            f"return_temp_lower={self.return_temp_lower}, "
            f"unit_flow={len(self.unit_flow)} items, "
            f"cal_frequency={self.cal_frequency} min)"
        )



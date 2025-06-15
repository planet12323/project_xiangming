TEST_URL = 'http://127.0.0.1'
PRODUCTION_URL = 'http://120.27.240.245:8900'
GET_API = {
    'meteorological-station': '/meteorological-station/real-time/v1',
    'temperature-terminal': '/temperature-terminal/real-time/v1',
    'weather-forecast': '/weather-forecast/24h/v1',
    'air-source-heat-pump': '/air-source-heat-pump/real-time/v1',
    'centrifuge': '/centrifuge/real-time/v1',
    'circulating-water-pump': '/circulating-water-pump/real-time/v1',
    'cooling-tower-fan': '/cooling-tower-fan/real-time/v1',
    # 'cooling-tower-fan': '/cooling-tower-fan/real-time/v1'
    'electrical-meter': '/electrical-meter/real-time/v1',
    'energy-meter': '/energy-meter/real-time/v1',
    "ground-source-heat-pump": "/ground-source-heat-pump/real-time/v1"
}

POST_API = {
    'payload-forecast': '/receive/payload-forecast/v1',
    'temperature-forecast': '/receive/temperature-forecast/v1',
    'air-source-heat-pump': '/receive/control-instruct/air-source-heat-pump/v1',
    'ground-source-heat-pump': '/receive/control-instruct/ground-source-heat-pump/v1',
    'centrifugal-chiller': '/receive/control-instruct/centrifugal-chiller/v1',
    'circulating-water-pump': '/receive/control-instruct/circulating-water-pump/v1',
    'cooling-tower-fan': '/receive/control-instruct/cooling-tower-fan/v1'
}

POST_PARAMS = {
    'payload-forecast': {
        'json_data': {
            "forecastType": 1,  # Int32
            "startTime": 1672531200,
            "endTime": 1672617600,
            "forecastDataList": [
                {
                    "value": 23.5,
                    "dataTime": 1672531200
                },
                {"value": 23.5,
                 "dataTime": 1672531200}
            ]
        }
    },
    'temperature-forecast': {
        'json_data': {
            'forecastType': 1,  # Int32
            'startTime': 0,
            'endTime': 0,
            'forecastDataList': [
                {
                    "value": 23.5,
                    "dataTime": 1672531200
                },
                {"value": 23.5,
                 "dataTime": 1672531200}
            ]
        }
    },
    'air-source-heat-pump': {
        'json_data': {
            'deviceId': 100000024775,  # Int32
            'operate': 1,
            'operateParam': 0,
            'dataTime': 1672531200
        }
    },
    'ground-source-heat-pump': {
        'json_data': {
            'deviceId': 100000024735,  # Int32
            'operate': 0,
            'operateParam': 0,
            'dataTime': 0
        }
    },
    'centrifugal-chiller': {
        'json_data': {
            'deviceId': 100000024724,  # Int32
            'operate': 0,
            'operateParam': 0,
            'dataTime': 0
        }
    },
    'circulating-water-pump': {
        'json_data': {
            'deviceId': 100000024806,  # Int32
            'operate': 0,
            'operateParam': 0,
            'dataTime': 0
        }
    },
    'cooling-tower-fan': {
        'json_data': {
            'deviceId': 100000024788,  # Int32
            'operate': 1,
            'dataTime': 0
        }
    }
}

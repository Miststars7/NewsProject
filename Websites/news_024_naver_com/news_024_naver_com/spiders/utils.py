# -*- coding: utf-8 -*-
import redis
import time
import hashlib
from datetime import datetime, timedelta
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

# 链接数据库
if settings['CURRENT_ENVIRONMENT'] == 'live':
    redis_0 = redis.StrictRedis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=settings['REDIS_DB'],
                                password=settings['REDIS_PASSWORD'])
else:
    redis_0 = redis.StrictRedis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=settings['REDIS_DB'])


def is_exist(key, value):
    value_md5 = md5(value)
    if redis_0.sismember(key, value_md5):
        return True
    else:
        redis_0.sadd(key, value_md5)
        return False


def current_timestamp():
    """当前时间戳 13位"""
    return int(time.time() * 1000)


def get_last_month_timestamps():
    """获取当前为止，到上个月到时间戳"""
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    one_month_ago = now - timedelta(days=30)
    return int(one_month_ago.strftime("%Y%m%d%H%M%S"))
    # one_month_ago_timestamp = int(time.mktime(one_month_ago.timetuple()))
    # return one_month_ago_timestamp


def convert_to_east_eight(time_str):
    """将这个网站格式的时间格式转换为东八区的年月日时分秒的格式"""
    # time_str = '2024-07-03 23:02:00'
    if not time_str:
        return time_str
    localtime = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    # 韩国与中国时差1小时
    east_eight_time = localtime - timedelta(hours=1)
    return east_eight_time


def convert_to_timestamp(date_str):
    """将特殊的时间格式转换为时间戳的格式"""
    date_format = '%d/%m/%y %H:%M'
    date_time_obj = datetime.strptime(date_str, date_format)
    timestamp = int(time.mktime(date_time_obj.timetuple()))
    return timestamp


def md5(content):
    """获取md5的值"""
    contents = str(content).encode('utf-8')
    md5_obj = hashlib.md5()
    md5_obj.update(contents)
    return md5_obj.hexdigest()

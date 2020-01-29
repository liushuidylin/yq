import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import json
import db
import schedule
import time


db = db.DB()

def get_indexes(_string: str, _char: str):
    """用来返回指定的_char在_string的全部索引
    """
    index_list = []
    for idx, char in enumerate(_string):
        if char == _char:
            index_list.append(idx)

    return index_list


class FetchData(object):
    def __init__(self):
        self.url = 'https://3g.dxy.cn/newh5/view/pneumonia'

    def get_one_page(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/73.0.3683.86 Safari/537.36'
            }
            r = requests.get(self.url, headers=headers)
            r.encoding = r.apparent_encoding
            if r.status_code == 200:
                return r.text
            return None
        except RequestException:
            return None

    def parse_one_page(self, html, now_time):
        doc = pq(html)
        area_stat = doc('#getAreaStat').text()
        first_index = area_stat.index('[')
        all_index = get_indexes(area_stat, ']')
        last_index = all_index[-1]+1
        yq_str = area_stat[first_index: last_index]
        yq_list = json.loads(yq_str)
        for yq_item in yq_list:
            province_short_name = yq_item['provinceShortName']
            yq_item['insertTime'] = now_time
            items = yq_item['cities']
            del yq_item['cities']
            db.insert('yq', yq_item)
            for item in items:
                item['insertTime'] = now_time
                item['provinceName'] = province_short_name
                db.insert('yq', item)


# 定义要执行的周期任务
def job():
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    fetch_data = FetchData()
    html = fetch_data.get_one_page()
    fetch_data.parse_one_page(html, now_time)


if __name__ == '__main__':
    schedule.every().day.at("21:07").do(job)
    while True:
        schedule.run_pending()  # 运行所有可以运行的任务

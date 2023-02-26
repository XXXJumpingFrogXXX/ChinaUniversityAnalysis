# 王麒翔数据科学项目代码
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pyecharts.charts import Bar, Pie, Geo, Liquid
from pyecharts.commons.utils import JsCode
from pyecharts import options as opts
from pyecharts.globals import ChartType, CurrentConfig, NotebookType
import os
import time


def get_attrs(data):
    college_name = data.find('strong')['title']
    college_attr = data.find_all('li')
    college_site = college_attr[0].text[6:]
    college_title = college_attr[1].text[5:]
    college_type = college_attr[2].text[5:]
    college_belong = college_attr[3].text[5:]
    college_nature = college_attr[4].text[5:]
    college_website = college_attr[5].text[5:]
    result = {
        'college_name': college_name,
        'college_site': college_site,
        'college_title': college_title,
        'college_type': college_type,
        'college_belong': college_belong,
        'college_nature': college_nature,
        'college_website': college_website
    }
    return result


def save_to_csv(data):
    if not os.path.exists(r'college_data.csv'):
        with open('college_data.csv', 'a+', encoding='utf-8') as f:
            f.write('name,site,title,type,belong,nature,website\n')
            for info in data:
                try:
                    row = '{},{},{},{},{},{},{}'.format(info['college_name'],
                                                        info['college_site'],
                                                        info['college_title'],
                                                        info['college_type'],
                                                        info['college_belong'],
                                                        info['college_nature'],
                                                        info['college_website'])
                    f.write(row)
                    f.write('\n')
                except:
                    continue
    else:
        with open('college_data.csv', 'a+', encoding='utf-8') as f:
            for info in data:
                try:
                    row = '{},{},{},{},{},{},{}'.format(info['college_name'],
                                                        info['college_site'],
                                                        info['college_title'],
                                                        info['college_type'],
                                                        info['college_belong'],
                                                        info['college_nature'],
                                                        info['college_website'])
                    f.write(row)
                    f.write('\n')
                except:
                    continue

def data_crawler():
    for i in range(1, 108):
        url = 'http://college.gaokao.com/schlist/p%s/' % i
        info = requests.get(url).text
        content = BeautifulSoup(info, 'html.parser')
        html_abstract_info = content.find('div', attrs={'class': 'scores_List'}).find_all('dl')
        college_info = map(get_attrs, html_abstract_info)
        save_to_csv(college_info)

        print('第%s页的数据信息已爬取完毕...' %i)
        time.sleep(1)

if __name__ == '__main__':
    CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
    data_crawler()
from pyecharts import options as opts
from pyecharts.charts import Map
import pandas as pd
import requests, json, re
import ast

#数据收集及处理
r = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5') #通过url获得疫情数据
state=json.loads(r.text) #解码转变为python对象

data = state['data'] # a为string类型
data = json.loads(data)

#变量分配
chinaTotal = data['chinaTotal']
chinaAdd = data['chinaAdd']
lastUpdateTime = data['lastUpdateTime']
specific_num = data['areaTree']
print('总数:',end='')
print(chinaTotal)
print('今天增加数量:',end='')
print(chinaAdd)
print('更新时间:',end='')
print(lastUpdateTime)

#数据分组及打印
province_list = []
N = specific_num[0]['children']
x = len(N)
for i in range(x):
    M = N[i]
    province_num = [M['name'],M['total'],M['today']]
    province_list.append((M['name'],M['total']['confirm']))

c = (
    Map()
    .add("",province_list,"china")
    .set_global_opts(title_opts = opts.TitleOpts(title = "(中国)肺炎确诊分布图"),
    visualmap_opts=opts.VisualMapOpts(  
        is_piecewise=True,  # 设置为分段
        pieces=[
        {"max":9, "min":1, "label": "1-9人"},
        {"max":99, "min":10, "label": "10-99人"},
        {"max":499, "min":100, "label": "100-499人"},
        {"max":999, "min":500, "label": "500-999人"},
        {"max":9999, "min":1000, "label": "1000-9999人"},
        {"max":99999, "min":10000, "label": "10000人以上"},
        ])
        )
    )

c.render('map.html')

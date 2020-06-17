#爬取58tc上重庆二手房的price square floors rooms subway area信息并保存为csv格式,存到文件 res.csv中
#@author smallsmart 
#GitHub地址: github.com/smallsmartlc

import requests
from bs4 import BeautifulSoup
import csv
import os 
with open('res.csv', mode='a',newline='') as csv_file:
    fieldnames = ['name', 'price', 'square','floors','rooms','subway', 'area']
    # 设置字段
    writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
    # writer.writeheader(); #写入csv标题,第一次爬数据时使用

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
    #1号线102,2号线103,3号线104,4号线196,5号线198,6号线105,10号线200,环线199
    #每次爬取时根据url
    url = 'https://cq.58.com/ershoufang/sub/pn2';#pnXX 指第x页
    r = requests.get(url=url, headers=headers)
    html = r.text        
    # html.parser解析器
    soup = BeautifulSoup(html, 'html.parser')
    con = soup.find('ul',class_='house-list-wrap')
    con_list = con.find_all('li' ,class_= 'sendsoj')
    con_list
    for i in con_list:
        name = i.find('h2',class_='title').find('a').get_text();
        price = i.find('div',class_='price').find('p',class_ = 'unit').get_text();
        list = i.find('div',class_='list-info').find('p',class_ = 'baseinfo').find_all('span');
        square = list[1].get_text();
        floors = list[3].get_text();
        rooms = list[0].get_text();
        subwaybox = i.find('div',class_='list-info').find_all('p',class_ = 'baseinfo')[1].find_all('span');
        subway = "";
        if len(subwaybox)>1 :
            subway = subwaybox[1].get_text();
        else :
            subway = "";
        area= i.find('div',class_='list-info').find_all('p',class_ = 'baseinfo')[1].find_all('a')[1].get_text();
        json = {'name': name.strip(),'price':price.strip() ,'square':square.strip(),'floors':floors.strip(),'rooms' : rooms.strip(),'subway': subway , 'area': area}
        print(json)#打印结果
        writer.writerow(json)#将结果写入csv


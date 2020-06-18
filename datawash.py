#对爬取的数据进行调整,把字符转成数字
# 读文件和写文件
#@author smallsmart 
#GitHub地址: github.com/smallsmartlc

import csv
import re

resf = csv.reader(open('res.csv','r'));
newf = open('res2.csv',mode='w',newline='');
fieldnames = ['price', 'square','floors','rooms','subway', 'area']
    # 设置字段
writer = csv.DictWriter(newf,fieldnames=fieldnames)
# writer = csv.writer(newf)
writer.writeheader(); #写入csv标题
a = 0;
dict = {'巴南区':1,'北碚区': 2,'璧山区': 3,'大渡口区': 4,'大足区':5,'垫江县':6,'涪陵区':7,'合川区':8,'江北区':9,'江津区':10,'九龙坡区':11,'开州区(开县)':12,'梁平县':13,'南岸区':14,'南川区':15,'荣昌区':16,'沙坪坝区':17,'铜梁区':18,'潼南区':19,'万州区':20,'永川区':21,'渝北区':22,'渝中区':23,'云阳县':24,'长寿区':25}#设置字典,通过数据来设定特征值
for i in resf:
    a=a+1
    if a == 1:
        continue;
    #使用正则表达式匹配数据
    price = re.compile('^[0-9]*').findall(i[1])[0]
    square = re.compile('[1-9]\d*\.\d*|0\.\d*[1-9]\d*').findall(i[2])[0]
    floors = re.compile('[0-9]+').findall(i[3])[0]
    rooms = int(re.compile('[0-9]+').findall(i[4])[0]) + int(re.compile('[0-9]+').findall(i[4])[1])+ int(re.compile('[0-9]+').findall(i[4])[2])
    #判断是否有地铁
    subway = 0;
    if len(i[5])>1:
        subway = 1;
    #通过字典设置区域的特征值
    area = dict[i[6]]
    json = {'price': price,'square':square,'floors':floors,'rooms':rooms,'subway':subway,'area':area}
    writer.writerow(json)#将处理好的数据写入
    print(json)



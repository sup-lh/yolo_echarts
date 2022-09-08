from tkinter import E
import pandas as pd
import redis
from time import sleep
import json
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

class OutputPower():
    async def run(self,s,websocket):
        while True:
            try:
                data_pie = r.hget('yolov7','webcam_pie')
                data_pie = [{'value':int(i.split(' ')[0]),'name':''.join(i.split(' ')[1:])} for i in [k.strip().strip("'").strip() for k in data_pie.strip('[]').split(',')]]
            except Exception as e:
                print(e)
                data_pie = []
            try:
                data_gauge = r.hget('yolov7','webcam_gauge')
                data_gauge = [[''.join(i[:-1]),int(float(i[-1])*100)] for i in [j.split(' ') for j in [k.strip().strip("'").strip() for k in data_gauge.strip('[]').split(',')]]]
                name_l = []
                value_l = []
                for i in data_gauge:
                    name_l.append(i[0])
                    value_l.append(i[1])
                data_gauge = [name_l,value_l]
            except Exception as e:
                print(e)
                data_gauge = []
            sleep(0.7)
        # 发送消息方法，单独和请求的客户端发消息
            await s(json.dumps({'data_pie':data_pie,'data_gauge':data_gauge}), websocket)

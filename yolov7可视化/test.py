from time import sleep
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
while True:
    data_gauge = r.hget('yolov7','webcam_gauge')
    data_gauge = [[''.join(i[:-1]),int(float(i[-1])*100)] for i in [j.split(' ') for j in [k.strip().strip("'").strip() for k in data_gauge.strip('[]').split(',')]]]

    name_l = []
    value_l = []
    for i in data_gauge:
        name_l.append(i[0])
        value_l.append(i[1])
    print(data_gauge)
    sleep(1)
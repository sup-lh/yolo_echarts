import redis,time
r = redis.Redis(host='127.0.0.1', port=6379)
while True:
    a = r.hgetall("data")
    for name,value in a.items():
        print(name.decode('utf-8'),value.decode('utf-8'))


    

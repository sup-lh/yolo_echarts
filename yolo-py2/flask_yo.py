import os
import json
import uuid
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask import request
import redis
import time

r = redis.Redis(host='127.0.0.1', port=6379)
app = Flask(__name__)
CORS(app, supports_credentials=True)


def read_result():
    with open('D:\\yes\\yolo-py2\\runs\\exp\\result.json', 'r')as f:
        fread = json.loads(f.read())['data']
        return fread


@app.route("/", methods=["POST"])
def file():
    try:
        files = request.files.getlist('files')
        imgname_list = []
        dirName = "images\\" + str(uuid.uuid4()).split("-")[-1]
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        for file in files:
            imgname = dirName + "\\" + str(uuid.uuid1())+".jpg"
            file.save(imgname)
            imgname_list.append(imgname)
        print("生成文件夹", dirName)
        os.system("python ../yolov7/detect.py --source " + dirName)
        read_list = read_result()
        print(read_list)
        return {
            "status": "ok",
            "imageName": imgname_list,
            "echartsData": read_list
        }
    except Exception as e:
        print(e)
        return {
            "status": "no"
        }


@app.route("/img", methods=["GET", "POST"])
def sendfile():
    name = request.args.get("name")
    print(name)
    filename = name.split("\\")[1]
    image = name.split("\\")[2]
    return send_from_directory("D:\\yes\\yolo-py2\\images\\"+filename, image)


@app.route("/yolo", methods=["GET", "POST"])
def yolo():
    name = request.args.get("name")
    print(name)

    image = name.split("\\")[2]
    print(image)
    return send_from_directory("D:\\yes\\yolo-py2\\runs\\exp", image)


@app.route("/monster", methods=["GET"])
def monster():
    imgname_list = []
    dirName = "images\\monster"
    imgname = dirName + "\\monster.jpg"
    imgname_list.append(imgname)
    os.system("python ../yolov7/detect.py --source " + dirName)
    read_list = read_result()
    return {
        "status": "ok",
        "imageName": imgname_list,
        "echartsData": read_list
    }


#远程摄像头搁浅
# @app.route("/webcam", methods=["GET"])
# def webcam():
#     link = request.args.get("link")
#     # 校验连接
#     print(link)
#     try:
#         a = os.system("python ../yolov7/detect_webcam.py --source " + link)
#         print(a)
#         return {
#             "status": "ok"
#         }
#     except Exception as e:
#         print(e)
#         return {
#             "status": "no"
#         }


if __name__ == "__main__":
    app.run("0.0.0.0", port=6677)

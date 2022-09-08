import os
# 拿到全部图片的绝对路径


def listFiles(dirPath):
    # 准备一个空列表，用来存储遍历数据
    fileList = []
    
    for root, dirs, files in os.walk(dirPath):
    
        # 循环遍历列表：files【所有文件】，仅得到不包含路径的文件名
        for fileObj in files:
        
            # 空列表写入遍历的文件名称，兵勇目录路径拼接文件名称
            fileList.append(os.path.join(root, fileObj))
            
    # 打印一下列表存储内容：指定文件夹下所有的文件名
    with open('val_list.txt','w',encoding='utf-8')as f:
        for i in fileList:
            print(i)
            f.write(i+'\n')
    # with open('train_list.txt','w',encoding='utf-8')as f:
    #     for i in fileList:
    #         print(i)
    #         f.write(i+'\n')

listFiles(r"C:\Users\Administrator\Desktop\yolov7\dataset\images\val")
# listFiles(r"C:\Users\Administrator\Desktop\yolov7\dataset\images\train")

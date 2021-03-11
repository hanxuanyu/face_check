import cv2
import os
import numpy as np
from PIL import Image  # pillow
import pyttsx3
import sys
import client.TcpClient as net


def makeDir(engine):
    if not os.path.exists("face_trainer"):
        print("创建预训练环境")
        engine.say('检测到第一次启动，未检测到环境，正在创建环境')
        engine.say('正在创建预训练环境')
        os.mkdir("face_trainer")
        engine.say('创建成功')
        engine.runAndWait()
    if not os.path.exists("Facedata"):
        print("创建训练环境")
        engine.say('正在创建训练环境')
        os.mkdir("Facedata")
        engine.say('创建成功')
        engine.runAndWait()
        return True
    return False


def getFace(cap, face_id):
    # 调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
    #cap = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #face_id = input('\n enter user id:')
    print('\n Initializing face capture. Look at the camera and wait ...')
    count = 0
    while True:
        # 从摄像头读取图片
        sucess, img = cap.read()
        # 转为灰度图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
            count += 1
            # 保存图像
            cv2.imwrite("Facedata/User." + str(face_id) + '.' + str(count) + '.jpg', gray[y: y + h, x: x + w])
            cv2.imshow('image', img)
        # 保持画面的持续。
        k = cv2.waitKey(1)
        if k == 27:   # 通过esc键退出摄像
            break
        elif count >= 100:  # 得到1000个样本后退出摄像
            break

    cv2.destroyAllWindows()

def getImagesAndLabels(path, detector):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # join函数的作用？
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            ids.append(id)
    return faceSamples, ids


def trainFace():
    # 人脸数据路径
    path = 'Facedata'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    print('训练人脸数据中，请稍候 ...')
    faces, ids = getImagesAndLabels(path,detector)
    recognizer.train(faces, np.array(ids))
    recognizer.write(r'face_trainer\trainer.yml')
    print("已经训练了 {0} 张人脸，正在退出训练系统".format(len(np.unique(ids))))

def say(engine,str):
    engine.say(str)
    engine.runAndWait()


if __name__ == '__main__':
    names = net.getNames()
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 20)
    isFirst = makeDir(engine)
    cam = cv2.VideoCapture(0)
    if isFirst:
        say(engine, "请输入您的姓名，注意要写成拼音形式")
        name = input("请输入姓名：")
        names.append(name)
        net.saveName(name)
        say(engine, "正在打开摄像头")

        say(engine, "注视摄像头，开始采集人脸数据")
        getFace(cam, len(names) - 1)
        say(engine, "采集完毕，开始训练")
        trainFace()
        say(engine, "训练完毕")
    cam.release()
    while True:
        say(engine, "是否要录入新的人脸信息      ")
        say(engine, "输入0 代表是 输入1 代表更新照片 其他代表不是")
        value = input("0：是 or other：否")
        if value == '0':
            say(engine, "请输入您的姓名，注意要写成拼音形式")
            name = input("请输入姓名：")
            names.append(name)
            net.saveName(name)
            say(engine, "正在打开摄像头")
            cam = cv2.VideoCapture(0)
            say(engine, "注视摄像头，开始采集人脸数据")
            getFace(cam, len(names) - 1)
            cam.release()
            say(engine, "采集完毕，开始训练")
            trainFace()
            say(engine, "训练完毕")
        elif value == '1':
            say(engine, "请输入您要更新的姓名，注意要写成拼音形式")
            name = input("请输入姓名：")
            count = 0
            for n in names:
                if name == n:
                    break
                count += 1
            say(engine, "正在打开摄像头")
            cam = cv2.VideoCapture(0)
            say(engine, "注视摄像头，开始采集人脸数据")
            getFace(cam, count)
            cam.release()
            say(engine, "采集完毕，开始训练")
            trainFace()
            say(engine, "训练完毕")
        else:
            say(engine, "再见")
            cam.release()
            sys.exit(0)





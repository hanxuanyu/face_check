import cv2
import pyttsx3
import sys
import client.TcpClient as net
import time


def say(engine,str):
    engine.say(str)
    engine.runAndWait()


def gettime():
    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(timeNow)
    return timeNow

def checkFace(cam, names, engine):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 100:
                idnum = names[idnum]
                date = gettime()
                flag = net.doSign(idnum, date)
                if flag:
                    print("欢迎      " + idnum + "于"+date+"签到成功！")
                    say(engine, "欢迎      " + idnum + "于"+date+"签到成功！")
                else:
                    print(idnum+"您已经签到成功，请勿重复签到")
                    say(engine, idnum+"您已经签到成功，请勿重复签到")
                return
            else:
                idnum = "unknown"
                confidence = "{0}%".format(round(100 - confidence))

            cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)
        cv2.imshow('camera', img)
        k = cv2.waitKey(10)
        if k == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    names = net.getNames()
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 20)
    cam = cv2.VideoCapture(0)

    while True:
        say(engine, "输入 0 开始签到 ，输入 其他任意键 退出系统")
        key = input("输入key：（0 - 开始签到 ，other - 退出系统）")
        if key == '0':
            checkFace(cam, names, engine)
        else:
            say(engine, "再见")
            sys.exit(0)
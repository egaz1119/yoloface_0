#!/usr/bin/env python
#-*- coding: utf-8 -*-

#人物を検知した時に画像を撮影して撮影画像をS3に送信する

import boto3
import json
import cv2
import datetime
import time
import numpy as np
import RPi.GPIO as GPIO
import os
import argparse
import shutil
import time
from PIL import Image
#from keras_yolo3.yolo import YOLO
#from objects import get_objects_information
#import tensorflow as tf

#人感センサ設定情報
INTAVAL = 3
SLEEPTIME = 5
SENSOR_PIN = 18
st = time.time()-INTAVAL

#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

#正面顔のHaar-like特徴分類器の保存先
CASCADE_PASS = 'models/haarcascade_frontalface_alt.xml'

#AWS関連設定情報
REGION = 'us-east-1'
ACCESS_KEY = 'AKIAJSCF5NR6AYIDS3GA'
SECRET_KEY = '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'
IMG_NAME = 'photo.jpg'
IMG_PASS = '/home/pi/workspace/yoloface-master/outputs/' + IMG_NAME
BUCKET_NAME = 'egaz'

def camera(NUM):    #webカメラで画像を1枚撮影し「NUM.jpg」として保存
    c = cv2.VideoCapture(0)
    r, img = c.read()
    T = datetime.datetime.now()
    NAME = str(NUM) + '.jpg'
    #cv2.imwrite(NAME, img)
    cv2.imwrite('/home/pi/workspace/yoloface-master/inputs/' + NAME, img)

def photo_take():       #0.5秒ごとに画像を１０枚撮影する。画像は"1.jpg"~"10.jpg"として保存
    for num in range(1,11):
        print (num)
        camera(num)
        time.sleep(0.5)

#def photo_up():         #AWS S3に画像"photo.jpg"をアップ
    #s3 = boto3.client('s3',region_name=REGION,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    #for dirpath, dirnames, filenames in os.walk(IMG_NAME):
        #for file in filenames:
            #IMG_PASS = dirpath + "/" + file
            #s3.upload_file(IMG_PASS,BUCKET_NAME,file)
            #print("uploaded {0}".format(file))
            #print("送信完了")
def photo_up():         #AWS S3に画像"photo.jpg"をアップ
    s3 = boto3.resource('s3',region_name=REGION,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    data = open('/home/pi/workspace/yoloface-master/outputs/' + IMG_NAME, 'rb')
    s3.Bucket(BUCKET_NAME).put_object(Key=IMG_NAME, Body=data)    



#while True:
if(os.path.exists('/home/pi/workspace/yoloface-master/outputs/photo.jpg')):
    print("画像をAWSへ送ります。")
    photo_up()
    print("送信完了")
    os.remove('/home/pi/workspace/yoloface-master/outputs/photo.jpg')
else:
    print('none')

GPIO.cleanup()
#time.sleep(SLEEPTIME)

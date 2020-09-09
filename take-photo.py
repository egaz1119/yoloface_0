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
ACCESS_KEY = ''
SECRET_KEY = ''
IMG_NAME = "./picture"
IMG_PASS = "./picture"
BUCKET_NAME = 'egaz'

def camera(NUM):    #webカメラで画像を1枚撮影し「NUM.jpg」として保存
    c = cv2.VideoCapture(0)
    r, img = c.read()
    T = datetime.datetime.now()
    NAME = str(NUM) + '.jpg'
    cv2.imwrite('/home/pi/workspace/yoloface-master/inputs/' + NAME, img)

def photo_take():       #0.5秒ごとに画像を１０枚撮影する。画像は"1.jpg"~"10.jpg"として保存
    for num in range(1,11):
        print (num)
        camera(num)
        time.sleep(0.5)

def photo_up():         #AWS S3に画像"photo.jpg"をアップ
    s3 = boto3.client('s3',region_name=REGION,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    for dirpath, dirnames, filenames in os.walk(IMG_NAME):
        for file in filenames:
            IMG_PASS = dirpath + "/" + file
            s3.upload_file(IMG_PASS,BUCKET_NAME,file)
            print("uploaded {0}".format(file))
    

print ("人感センサー起動中")

#while True:
face_cascade = cv2.CascadeClassifier(CASCADE_PASS)
print ("...")
if(GPIO.input(SENSOR_PIN) == GPIO.HIGH) and (st + INTAVAL < time.time()) and (__name__=='__main__'):
     #n = 1
    #st = time.time()   
    print("人を感知しました。撮影します。")
    photo_take()
    print("顔を探しています...")

GPIO.cleanup()
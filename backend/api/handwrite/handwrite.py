# -*- coding: utf-8 -*-
"""
@author: wangshujing
"""
import os
import cv2
import numpy as np

# 添加当前项目到环境变量
import sys
sys.path.append(os.path.join(os.getcwd(),"backend","api","handwrite"))
from dnn.main import text_ocr
from hwconfig import scale,maxScale,TEXT_LINE_SCORE

class HandWrite:
    """手写体识别"""
    def __init__(self):
        self = self

    def getWord(self, img_file):
        img = cv2.imread(img_file)##GBR
        # print (img_file)
        # print (img)
        if img is not None:
            image = np.array(img)
            image =  cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            data = text_ocr(image,scale,maxScale,TEXT_LINE_SCORE)

            res = {'data':data,'errCode':0}
        else:
            res = {'data':[],'errCode':3}
        return res


if __name__ == '__main__':
    handWriteTest = HandWrite()
    handword = handWriteTest.getWord(os.path.join(os.getcwd(),"backend","api","handwrite","test","img.jpeg"))

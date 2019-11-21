"""
created by: xiongjian
"""

from __future__ import print_function
import os
import argparse
import numpy as np
import pandas as pd
import time
import shutil
import uuid
import cv2
from PIL import Image
from io import BytesIO
import json
from PIL import Image
from tqdm import tqdm
import torch
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torchvision.models as models
from django.conf import settings
from decimal import Decimal
from decimal import getcontext
from moviepy.editor import VideoFileClip
import subprocess
import math


class video:
    def __init__(self):
        self = self

    def get_two_float(self, f_str, n):
        f_str = str(f_str)      # f_str = '{}'.format(f_str) 也可以转换为字符串
        a, b, c = f_str.partition('.')
        c = (c+"0"*n)[:n]       # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
        return ".".join([a, c])

    # 获取图片旋转角度
    def get_minAreaRect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh > 0))
        return cv2.minAreaRect(coords)

    # 图片旋转
    def rotate_bound(self, image, angle):
        # 获取宽高
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # 提取旋转矩阵 sin cos
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # 计算图像的新边界尺寸
        nW = int((h * sin) + (w * cos))
        # nH = int((h * cos) + (w * sin))
        nH = h

        # 调整旋转矩阵
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        return cv2.warpAffine(image, M, (nW, nH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def RunShellWithReturnCode(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        p.wait()
        output = ""
        while True:
            line = p.stdout.read()
            if not line:
                break
            output += line.decode("utf-8")
        # print(output)
        return output

    def convert_avi_to_mp4(self, avi_file_path, output_name):
        try:
            fsize = os.path.getsize(avi_file_path)
            if fsize > 0:
                cmd = "ffmpeg -i {input} -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 {output}.mp4".format(
                    input=avi_file_path, output=output_name)
                out = self.RunShellWithReturnCode(cmd)
                return True
            else:
                print("传入的文件格式不对")
                return False
        except:
            print("传入的文件格式不对")
            return False

    def convert_mov_to_mp4(self, mov_file_path, output_name):
        try:
            fsize = os.path.getsize(avi_file_path)
            if fsize > 0:
                cmd = "ffmpeg -i {input} -q:v 0 -f mp4 {output}.mp4".format(
                    input=mov_file_path, output=output_name)
                out = self.RunShellWithReturnCode(cmd)
                return True
            else:
                print("传入的文件格式不对")
                return False
        except:
            print("传入的文件格式不对")
            return False

    def check_video(self, file_path, orientation, serial_number):
        t = time.time()
        startTime = int(round(t * 1000))

        # 转换视频
        if file_path.endswith('.avi'):
            fileNameMp4 = file_path.replace('.avi', '')
            convertReulst = self.convert_avi_to_mp4(file_path, fileNameMp4)
            if convertReulst:
                file_path = fileNameMp4 + '.mp4'
        elif file_path.endswith('.mov'):
            fileNameMp4 = file_path.replace('.mov', '')
            convertReulst = self.convert_mov_to_mp4(file_path, fileNameMp4)
            if convertReulst:
                file_path = fileNameMp4 + '.mp4'

        # 读取视频
        totalCount = 0
        pornTotalCount = 0
        cap = cv2.VideoCapture(file_path)

        clip = VideoFileClip(file_path)
        # 获取FPS(每秒传输帧数(Frames Per Second))
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 获取总帧数
        totalFrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print("fps=", fps)
        print("totalFrameNumber=", totalFrameNumber)
        # 当前读取到第几帧
        p, f = os.path.split(file_path)
        COUNT = 0
        uuidStr = str(uuid.uuid1())
        temp_path = settings.SAVE_PATH+uuidStr+"/"
        os.makedirs(temp_path)  # 重新创建文件夹
        contentList = []
        violenceList = []
        pornList = []
        violenceScoreArr = [0.00]*int(totalFrameNumber)
        pornScoreArr = [0.00]*int(totalFrameNumber)
        FPS_FLAG = settings.FPS_FLAG  # 为True时，按帧读取；False时，按秒读取
        # 暴恐级别比例
        VIOLENCESCORE_MIN = settings.VIOLENCESCORE_MIN
        VIOLENCESCORE_MAX = settings.VIOLENCESCORE_MAX
        # 色情级别比例
        PORNSCORE_MIN = settings.PORNSCORE_MIN
        PORNSCORE_MAX = settings.PORNSCORE_MAX
        if FPS_FLAG:
            # 若小于总帧数则读一帧图像
            while COUNT < totalFrameNumber:
                contentMap = {}
                # 一帧一帧图像读取
                ret, frame = cap.read()
                # 把每一帧图像保存成jpg格式（这一行可以根据需要选择保留）
                imageName = str(COUNT) + '.jpg'
                try:
                    # 增加图片旋转矫正
                    if orientation:
                        # Flipped Horizontally 水平翻转
                        if orientation == 3:
                            frame = self.rotate_bound(frame, 180.000)
                        elif orientation == 6:
                            frame = self.rotate_bound(frame, -90.000)
                        elif orientation == 8:
                            frame = self.rotate_bound(frame, 90.000)

                    cv2.imwrite(temp_path+imageName, frame)
                    jsonResultInfo = settings.VIOLENCE.check_violence(
                        temp_path + '/' + imageName)
                    violencePercent = jsonResultInfo.get('violence')
                    violenceScore = float(violencePercent)
                    pornPercent = settings.NSFW.caffe_preprocess_and_compute_api(
                        temp_path+imageName)
                    violenceScoreArr[COUNT] = violenceScore
                    pornScore = "%.2f" % float(pornPercent[1])
                    pornScore = float(pornScore)
                    #pornScore = "%.2f" % float(pornPercent[1])
                    contentMap = {}

                    pornScoreArr[COUNT] = pornScore

                    infoMap = {}
                    violenceMap = {}
                    pornMap = {}
                    if (violenceScore >= settings.VIOLENCESCORE_MIN or pornScore >= settings.PORNSCORE_MIN):
                        infoMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        infoMap['porn_sensitivity_level'] = self.get_two_float(
                            float(pornPercent[1]) * 100, 2)
                        infoMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        infoMap['sensitivity_time'] = self.get_two_float(
                            (COUNT+1) / fps, 2)
                        infoMap['current_fps'] = COUNT
                        contentList.append(infoMap)

                    if (violenceScore >= settings.VIOLENCESCORE_MIN):
                        violenceMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        violenceMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        violenceMap['sensitivity_time'] = self.get_two_float(
                            (COUNT+1) / fps, 2)
                        violenceMap['current_fps'] = COUNT
                        violenceList.append(violenceMap)

                    if (pornScore >= settings.PORNSCORE_MIN):
                        pornMap['porn_sensitivity_level'] = self.get_two_float(
                            pornPercent[1] * 100, 2)
                        pornMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        pornMap['sensitivity_time'] = self.get_two_float(
                            (COUNT+1) / fps, 2)
                        pornMap['current_fps'] = COUNT
                        pornList.append(pornMap)

                    COUNT = COUNT + 1
                    # if COUNT>3:
                    #    violencePercent=0
                    # 延时一段33ms（1s?30帧）再读取下一帧，如果没有这一句便无法正常显示视频
                    cv2.waitKey(33)
                except:
                    continue
            cap.release()
            pornScoreArr = sorted(pornScoreArr)
            violenceScoreArr = sorted(violenceScoreArr)
            violence_sensitivity_level = 0
            if (violenceScoreArr[-1] < VIOLENCESCORE_MIN):
                violence_sensitivity_level = 0
            elif (violenceScoreArr[-1] >= VIOLENCESCORE_MIN and violenceScoreArr[-1] <= VIOLENCESCORE_MAX):
                violence_sensitivity_level = 1
            elif (violenceScoreArr[-1] > VIOLENCESCORE_MAX):
                violence_sensitivity_level = 2

            porn_sensitivity_level = 0
            if (pornScoreArr[-1] < PORNSCORE_MIN):
                porn_sensitivity_level = 0
            elif (pornScoreArr[-1] >= PORNSCORE_MIN and pornScoreArr[-1] <= PORNSCORE_MAX):
                porn_sensitivity_level = 1
            elif (pornScoreArr[-1] > PORNSCORE_MAX):
                porn_sensitivity_level = 2
            resultMap = {}

            # 增加最大敏感类型
            if float(violenceScoreArr[-1]) > float(pornScoreArr[-1]):
                max_sensitivity_type = 'violence'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]
            elif float(violenceScoreArr[-1]) < float(pornScoreArr[-1]):
                max_sensitivity_type = 'porn'
                max_sensitivity_level = porn_sensitivity_level
                max_sensitivity_percent = pornScoreArr[-1]
            else:
                max_sensitivity_type = 'violence_porn'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]

            resultMap['video_url'] = settings.VIDEO_URL + f
            resultMap['violence_sensitivity_level'] = violence_sensitivity_level
            resultMap['porn_sensitivity_level'] = porn_sensitivity_level
            resultMap['video_evidence_information'] = contentList
            resultMap['violence_evidence_information'] = violenceList
            resultMap['porn_evidence_information'] = pornList
            resultMap['interval'] = self.get_two_float(float(self.get_two_float(
                (COUNT+1) / fps, 2)) - float(self.get_two_float((COUNT) / fps, 2)), 3)
            resultMap['duration'] = int(clip.duration)
            resultMap['fps'] = fps
            t = time.time()
            endTime = int(round(t * 1000))
            print(endTime - startTime)
            resultMap['taketimes'] = endTime - startTime
            resultMap['max_sensitivity_type'] = max_sensitivity_type
            resultMap['max_sensitivity_level'] = max_sensitivity_level
            resultMap['violence_percent'] = self.get_two_float(violenceScoreArr[-1], 2)
            resultMap['porn_percent'] = self.get_two_float(pornScoreArr[-1], 2)
            resultMap['screenshot_url'] = settings.VIDEO_URL + \
                settings.TEMP_PATH + uuidStr + "/" + "0.jpg"
            resultMap['serial_number'] = serial_number
            # contentMap['politics_ sensitivity_level'] =
            # shutil.rmtree(temp_path)
            # print(totalCount)

        else:
            c = 1
            if cap.isOpened():  # 判断是否正常打开
                rval, frame = cap.read()
            else:
                rval = False
            timeF = fps  # 视频帧计数间隔频率

            while rval:  # 循环读取视频帧
                #pic_path = temp_path + '/'
                if (c % timeF == 0 or c == 1):  # 每隔timeF帧进行存储操作
                    imageName = str(COUNT) + '.jpg'

                    # 增加图片旋转矫正
                    if orientation:
                        # Flipped Horizontally 水平翻转
                        if orientation == 3:
                            frame = self.rotate_bound(frame, 180.000)
                        elif orientation == 6:
                            frame = self.rotate_bound(frame, -90.000)
                        elif orientation == 8:
                            frame = self.rotate_bound(frame, 90.000)

                    cv2.imwrite(temp_path + '/' + imageName, frame)  # 存储图像

                    jsonResultInfo = settings.VIOLENCE.check_violence(
                        temp_path + '/' + imageName)
                    violencePercent = jsonResultInfo.get('violence')
                    violenceScore = float(violencePercent)
                    pornPercent = settings.NSFW.caffe_preprocess_and_compute_api(
                        temp_path+imageName)
                    pornScore = "%.2f" % float(pornPercent[1])
                    pornScore = float(pornScore)
                    violenceScoreArr[COUNT] = violenceScore
                    pornScoreArr[COUNT] = pornScore
                    infoMap = {}
                    violenceMap = {}
                    pornMap = {}
                    if (violenceScore >= settings.VIOLENCESCORE_MIN or pornScore >= settings.PORNSCORE_MIN):
                        infoMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        infoMap['porn_sensitivity_level'] = self.get_two_float(
                            float(pornPercent[1]) * 100, 2)
                        infoMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        infoMap['sensitivity_time'] = self.get_two_float(
                            COUNT, 2)
                        infoMap['current_fps'] = c+1
                        contentList.append(infoMap)

                    if (violenceScore >= settings.VIOLENCESCORE_MIN):
                        violenceMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        violenceMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        violenceMap['sensitivity_time'] = self.get_two_float(
                            COUNT, 2)
                        violenceMap['current_fps'] = c+1
                        violenceList.append(violenceMap)

                    if (pornScore >= settings.PORNSCORE_MIN):
                        pornMap['porn_sensitivity_level'] = self.get_two_float(
                            pornPercent[1] * 100, 2)
                        pornMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        pornMap['sensitivity_time'] = self.get_two_float(
                            COUNT, 2)
                        pornMap['current_fps'] = c+1
                        pornList.append(pornMap)

                    COUNT = COUNT + 1
                c = c + 1
                cv2.waitKey(1)
                rval, frame = cap.read()
            cap.release()
            # 判断暴恐图片
            pornScoreArr = sorted(pornScoreArr)
            violenceScoreArr = sorted(violenceScoreArr)
            violence_sensitivity_level = 0
            if (violenceScoreArr[-1] < VIOLENCESCORE_MIN):
                violence_sensitivity_level = 0
            elif (violenceScoreArr[-1] >= VIOLENCESCORE_MIN and violenceScoreArr[-1] <= VIOLENCESCORE_MAX):
                violence_sensitivity_level = 1
            elif (violenceScoreArr[-1] > VIOLENCESCORE_MAX):
                violence_sensitivity_level = 2

            # 判断色情图片
            porn_sensitivity_level = 0
            if (pornScoreArr[-1] < PORNSCORE_MIN):
                porn_sensitivity_level = 0
            elif (pornScoreArr[-1] >= PORNSCORE_MIN and pornScoreArr[-1] <= PORNSCORE_MAX):
                porn_sensitivity_level = 1
            elif (pornScoreArr[-1] > PORNSCORE_MAX):
                porn_sensitivity_level = 2

            # 增加最大敏感类型
            if float(violenceScoreArr[-1]) > float(pornScoreArr[-1]):
                max_sensitivity_type = 'violence'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]
            elif float(violenceScoreArr[-1]) < float(pornScoreArr[-1]):
                max_sensitivity_type = 'porn'
                max_sensitivity_level = porn_sensitivity_level
                max_sensitivity_percent = pornScoreArr[-1]
            else:
                max_sensitivity_type = 'violence_porn'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]

            resultMap = {}
            resultMap['video_url'] = settings.VIDEO_URL + f
            resultMap['violence_sensitivity_level'] = violence_sensitivity_level
            resultMap['porn_sensitivity_level'] = porn_sensitivity_level
            resultMap['video_evidence_information'] = contentList
            resultMap['violence_evidence_information'] = violenceList
            resultMap['porn_evidence_information'] = pornList
            resultMap['interval'] = self.get_two_float(float(self.get_two_float(
                (COUNT+1) / fps, 2)) - float(self.get_two_float((COUNT) / fps, 2)), 3)
            resultMap['duration'] = int(clip.duration)
            resultMap['fps'] = fps
            t = time.time()
            endTime = int(round(t * 1000))
            print(endTime - startTime)
            resultMap['taketimes'] = endTime - startTime
            resultMap['max_sensitivity_type'] = max_sensitivity_type
            resultMap['max_sensitivity_level'] = max_sensitivity_level
            resultMap['max_sensitivity_percent'] = max_sensitivity_percent
            resultMap['violence_percent'] = self.get_two_float(violenceScoreArr[-1], 2)
            resultMap['porn_percent'] = self.get_two_float(pornScoreArr[-1], 2)
            resultMap['screenshot_url'] = settings.VIDEO_URL + \
                settings.TEMP_PATH + uuidStr + "/" + "0.jpg"
            resultMap['serial_number'] = serial_number
        return resultMap

    def check_video_V2(self, file_path, orientation, serial_number):
        t = time.time()
        startTime = int(round(t * 1000))

        # 转换视频
        if file_path.endswith('.avi'):
            fileNameMp4 = file_path.replace('.avi', '')
            convertReulst = self.convert_avi_to_mp4(file_path, fileNameMp4)
            if convertReulst:
                file_path = fileNameMp4 + '.mp4'
        elif file_path.endswith('.mov'):
            fileNameMp4 = file_path.replace('.mov', '')
            convertReulst = self.convert_mov_to_mp4(file_path, fileNameMp4)
            if convertReulst:
                file_path = fileNameMp4 + '.mp4'

        # 读取视频
        totalCount = 0
        pornTotalCount = 0
        cap = cv2.VideoCapture(file_path)

        clip = VideoFileClip(file_path)
        # 获取FPS(每秒传输帧数(Frames Per Second))
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 获取总帧数
        totalFrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print("fps=", fps)
        print("totalFrameNumber=", totalFrameNumber)
        # 当前读取到第几帧
        p, f = os.path.split(file_path)
        uuidStr = str(uuid.uuid1())
        temp_path = settings.SAVE_PATH+uuidStr+"/"
        os.makedirs(temp_path)  # 重新创建文件夹
        contentList = []
        violenceList = []
        pornList = []
        violenceScoreArr = [0.00]*int(totalFrameNumber)
        pornScoreArr = [0.00]*int(totalFrameNumber)
        FPS_FLAG = settings.FPS_FLAG  # 为True时，按帧读取；False时，按秒读取
        # 暴恐级别比例
        VIOLENCESCORE_MIN = settings.VIOLENCESCORE_MIN
        VIOLENCESCORE_MAX = settings.VIOLENCESCORE_MAX
        # 色情级别比例
        PORNSCORE_MIN = settings.PORNSCORE_MIN
        PORNSCORE_MAX = settings.PORNSCORE_MAX
        # 识别计数
        COUNT = 0
        img_paths = []
        img_names = []
        jsonResultInfos = []

        if FPS_FLAG:
            # 针对暴恐增加批量识别功能
            while COUNT < totalFrameNumber:
                # 一帧一帧图像读取
                ret, frame = cap.read()
                # 把每一帧图像保存成jpg格式（这一行可以根据需要选择保留）
                imageName = str(COUNT) + '.jpg'
                cv2.imwrite(temp_path+imageName, frame)
                filename = temp_path + '/' + imageName
                filesize = os.stat(filename).st_size
                # 增加文件大小为0判断，如果大小为0，则忽略
                if filesize == 0:
                    totalFrameNumber = totalFrameNumber - 1
                else:
                    img_path = temp_path + '/' + imageName
                    img_names.append(imageName)
                    img_paths.append(img_path)
                    COUNT += 1

            COUNT = 0
            jsonResultInfos = settings.VIOLENCE.check_violences(img_paths)[
                "result"]

            # 若小于总帧数则读一帧图像
            while COUNT < totalFrameNumber:
                imageName = img_names[COUNT]
                imagePath = img_paths[COUNT]
                try:
                    # 增加图片旋转矫正
                    if orientation:
                        # Flipped Horizontally 水平翻转
                        if orientation == 3:
                            frame = self.rotate_bound(frame, 180.000)
                        elif orientation == 6:
                            frame = self.rotate_bound(frame, -90.000)
                        elif orientation == 8:
                            frame = self.rotate_bound(frame, 90.000)

                    if jsonResultInfos != False:
                        jsonResultInfo = jsonResultInfos[COUNT]
                        violencePercent = jsonResultInfo.get('violence')
                    else:
                        violencePercent = 0
                    violenceScore = float(violencePercent)
                    violenceScoreArr[COUNT] = violenceScore

                    pornPercent = settings.NSFW.caffe_preprocess_and_compute_api(
                        imagePath)
                    # pornScore = "%.2f" % float(pornPercent[1])
                    pornScore = math.floor(float(pornPercent[1])*10000)/100
                    # pornScore = float(pornScore)
                    pornScoreArr[COUNT] = pornScore

                    contentMap = {}
                    infoMap = {}
                    violenceMap = {}
                    pornMap = {}
                    if (violenceScore >= settings.VIOLENCESCORE_MIN or pornScore >= settings.PORNSCORE_MIN):
                        infoMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        infoMap['porn_sensitivity_level'] = self.get_two_float(
                            float(pornPercent[1]) * 100, 2)
                        infoMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        infoMap['sensitivity_time'] = self.get_two_float(
                            (COUNT+1) / fps, 2)
                        infoMap['current_fps'] = COUNT
                        contentList.append(infoMap)

                    if (violenceScore >= settings.VIOLENCESCORE_MIN):
                        violenceMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        violenceMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        violenceMap['sensitivity_time'] = self.get_two_float(
                            (COUNT+1) / fps, 2)
                        violenceMap['current_fps'] = COUNT
                        violenceList.append(violenceMap)

                    if (pornScore >= settings.PORNSCORE_MIN):
                        pornMap['porn_sensitivity_level'] = self.get_two_float(
                            pornPercent[1] * 100, 2)
                        pornMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        pornMap['sensitivity_time'] = self.get_two_float(
                            (COUNT+1) / fps, 2)
                        pornMap['current_fps'] = COUNT
                        pornList.append(pornMap)

                    COUNT = COUNT + 1
                    cv2.waitKey(33)
                except:
                    continue
            cap.release()
            pornScoreArr = sorted(pornScoreArr)
            violenceScoreArr = sorted(violenceScoreArr)
            violence_sensitivity_level = 0
            if (violenceScoreArr[-1] < VIOLENCESCORE_MIN):
                violence_sensitivity_level = 0
            elif (violenceScoreArr[-1] >= VIOLENCESCORE_MIN and violenceScoreArr[-1] <= VIOLENCESCORE_MAX):
                violence_sensitivity_level = 1
            elif (violenceScoreArr[-1] > VIOLENCESCORE_MAX):
                violence_sensitivity_level = 2

            porn_sensitivity_level = 0
            if (pornScoreArr[-1] < PORNSCORE_MIN):
                porn_sensitivity_level = 0
            elif (pornScoreArr[-1] >= PORNSCORE_MIN and pornScoreArr[-1] <= PORNSCORE_MAX):
                porn_sensitivity_level = 1
            elif (pornScoreArr[-1] > PORNSCORE_MAX):
                porn_sensitivity_level = 2
            resultMap = {}

            # 增加最大敏感类型
            if float(violenceScoreArr[-1]) > float(pornScoreArr[-1]):
                max_sensitivity_type = 'violence'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]
            elif float(violenceScoreArr[-1]) < float(pornScoreArr[-1]):
                max_sensitivity_type = 'porn'
                max_sensitivity_level = porn_sensitivity_level
                max_sensitivity_percent = pornScoreArr[-1]
            else:
                max_sensitivity_type = 'violence_porn'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]

            resultMap['video_url'] = settings.VIDEO_URL + f
            resultMap['violence_sensitivity_level'] = violence_sensitivity_level
            resultMap['porn_sensitivity_level'] = porn_sensitivity_level
            resultMap['video_evidence_information'] = contentList
            resultMap['violence_evidence_information'] = violenceList
            resultMap['porn_evidence_information'] = pornList
            resultMap['interval'] = self.get_two_float(float(self.get_two_float(
                (COUNT+1) / fps, 2)) - float(self.get_two_float((COUNT) / fps, 2)), 3)
            resultMap['duration'] = int(clip.duration)
            resultMap['fps'] = fps
            t = time.time()
            endTime = int(round(t * 1000))
            print(endTime - startTime)
            resultMap['taketimes'] = endTime - startTime
            resultMap['max_sensitivity_type'] = max_sensitivity_type
            resultMap['max_sensitivity_level'] = max_sensitivity_level
            resultMap['violence_percent'] = self.get_two_float(violenceScoreArr[-1], 2)
            resultMap['porn_percent'] = self.get_two_float(pornScoreArr[-1], 2)
            resultMap['screenshot_url'] = settings.VIDEO_URL + \
                settings.TEMP_PATH + uuidStr + "/" + "0.jpg"
            resultMap['serial_number'] = serial_number

        else:
            COUNT_SECOND = 1

            if cap.isOpened():  # 判断是否正常打开
                rval, frame = cap.read()
            else:
                rval = False
            timeF = fps  # 视频帧计数间隔频率

            # 针对暴恐增加批量识别功能
            while COUNT < totalFrameNumber:
                if (COUNT_SECOND % timeF == 0 or COUNT_SECOND == 1):  # 每隔timeF帧进行存储操作
                    rval, frame = cap.read()
                    imageName = str(COUNT) + '.jpg'
                    cv2.imwrite(temp_path+imageName, frame)

                    filename = temp_path + '/' + imageName
                    filesize = os.stat(filename).st_size
                    # 增加文件大小为0判断，如果大小为0，则忽略
                    if filesize == 0:
                        totalFrameNumber = totalFrameNumber - 1
                    else:
                        img_path = temp_path + '/' + imageName
                        img_names.append(imageName)
                        img_paths.append(img_path)
                        COUNT += 1
                COUNT_SECOND += 1

            COUNT_SECOND = 1
            COUNT = 0
            jsonResultInfos = settings.VIOLENCE.check_violences(img_paths)[
                "result"]

            while rval:  # 循环读取视频帧
                #pic_path = temp_path + '/'
                if (COUNT_SECOND % timeF == 0 or COUNT_SECOND == 1):  # 每隔timeF帧进行存储操作
                    imageName = img_names[COUNT]
                    imagePath = img_paths[COUNT]

                    # 增加图片旋转矫正
                    if orientation:
                        # Flipped Horizontally 水平翻转
                        if orientation == 3:
                            frame = self.rotate_bound(frame, 180.000)
                        elif orientation == 6:
                            frame = self.rotate_bound(frame, -90.000)
                        elif orientation == 8:
                            frame = self.rotate_bound(frame, 90.000)

                    if jsonResultInfos != False:
                        jsonResultInfo = jsonResultInfos[COUNT]
                        violencePercent = jsonResultInfo.get('violence')
                    else:
                        violencePercent = 0
                    violenceScore = float(violencePercent)
                    violenceScoreArr[COUNT] = violenceScore

                    pornPercent = settings.NSFW.caffe_preprocess_and_compute_api(
                        imagePath)
                    pornScore = "%.2f" % float(pornPercent[1])
                    pornScore = float(pornScore)
                    pornScoreArr[COUNT] = pornScore
                    infoMap = {}
                    violenceMap = {}
                    pornMap = {}
                    if (violenceScore >= settings.VIOLENCESCORE_MIN or pornScore >= settings.PORNSCORE_MIN):
                        infoMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        infoMap['porn_sensitivity_level'] = self.get_two_float(
                            float(pornPercent[1]) * 100, 2)
                        infoMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        infoMap['sensitivity_time'] = self.get_two_float(
                            COUNT, 2)
                        infoMap['current_fps'] = c+1
                        contentList.append(infoMap)

                    if (violenceScore >= settings.VIOLENCESCORE_MIN):
                        violenceMap['violence_sensitivity_level'] = self.get_two_float(
                            violenceScore * 100, 2)
                        violenceMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        violenceMap['sensitivity_time'] = self.get_two_float(
                            COUNT, 2)
                        violenceMap['current_fps'] = c+1
                        violenceList.append(violenceMap)

                    if (pornScore >= settings.PORNSCORE_MIN):
                        pornMap['porn_sensitivity_level'] = self.get_two_float(
                            pornPercent[1] * 100, 2)
                        pornMap['image_url'] = settings.VIDEO_URL + \
                            settings.TEMP_PATH + uuidStr + '/' + imageName
                        pornMap['sensitivity_time'] = self.get_two_float(
                            COUNT, 2)
                        pornMap['current_fps'] = c+1
                        pornList.append(pornMap)

                    COUNT = COUNT + 1
                COUNT_SECOND = COUNT_SECOND + 1
                rval, frame = cap.read()
            cap.release()
            # 判断暴恐图片
            pornScoreArr = sorted(pornScoreArr)
            violenceScoreArr = sorted(violenceScoreArr)
            violence_sensitivity_level = 0
            if (violenceScoreArr[-1] < VIOLENCESCORE_MIN):
                violence_sensitivity_level = 0
            elif (violenceScoreArr[-1] >= VIOLENCESCORE_MIN and violenceScoreArr[-1] <= VIOLENCESCORE_MAX):
                violence_sensitivity_level = 1
            elif (violenceScoreArr[-1] > VIOLENCESCORE_MAX):
                violence_sensitivity_level = 2

            # 判断色情图片
            porn_sensitivity_level = 0
            if (pornScoreArr[-1] < PORNSCORE_MIN):
                porn_sensitivity_level = 0
            elif (pornScoreArr[-1] >= PORNSCORE_MIN and pornScoreArr[-1] <= PORNSCORE_MAX):
                porn_sensitivity_level = 1
            elif (pornScoreArr[-1] > PORNSCORE_MAX):
                porn_sensitivity_level = 2

            # 增加最大敏感类型
            if float(violenceScoreArr[-1]) > float(pornScoreArr[-1]):
                max_sensitivity_type = 'violence'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]
            elif float(violenceScoreArr[-1]) < float(pornScoreArr[-1]):
                max_sensitivity_type = 'porn'
                max_sensitivity_level = porn_sensitivity_level
                max_sensitivity_percent = pornScoreArr[-1]
            else:
                max_sensitivity_type = 'violence_porn'
                max_sensitivity_level = violence_sensitivity_level
                max_sensitivity_percent = violenceScoreArr[-1]

            resultMap = {}
            resultMap['video_url'] = settings.VIDEO_URL + f
            resultMap['violence_sensitivity_level'] = violence_sensitivity_level
            resultMap['porn_sensitivity_level'] = porn_sensitivity_level
            resultMap['video_evidence_information'] = contentList
            resultMap['violence_evidence_information'] = violenceList
            resultMap['porn_evidence_information'] = pornList
            resultMap['interval'] = self.get_two_float(float(self.get_two_float(
                (COUNT+1) / fps, 2)) - float(self.get_two_float((COUNT) / fps, 2)), 3)
            resultMap['duration'] = int(clip.duration)
            resultMap['fps'] = fps
            t = time.time()
            endTime = int(round(t * 1000))
            print(endTime - startTime)
            resultMap['taketimes'] = endTime - startTime
            resultMap['max_sensitivity_type'] = max_sensitivity_type
            resultMap['max_sensitivity_level'] = max_sensitivity_level
            resultMap['max_sensitivity_percent'] = max_sensitivity_percent
            resultMap['violence_percent'] = self.get_two_float(violenceScoreArr[-1], 2)
            resultMap['porn_percent'] = self.get_two_float(pornScoreArr[-1], 2)
            resultMap['screenshot_url'] = settings.VIDEO_URL + \
                settings.TEMP_PATH + uuidStr + "/" + "0.jpg"
            resultMap['serial_number'] = serial_number
        return resultMap


if __name__ == '__main__':
    img_file = os.path.join(os.getcwd(), "backend", "api",
                            "yahoo", "open_nsfw", "images", "auW8xgi.jpg")
    image = cv2.imread(img_file)
    myvideo = video()
    angle = myvideo.get_minAreaRect(image)[-1]
    print(angle)
    print(type(angle))
    rotated = myvideo.rotate_bound(image, angle)
    cv2.putText(rotated, "angle: {:.2f} ".format(angle),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))
    cv2.imshow("imput", image)
    cv2.imshow("output", rotated)
    cv2.waitKey(0)

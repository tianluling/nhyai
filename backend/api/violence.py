"""
created by: Wangshujing
"""

from __future__ import print_function
import os
import argparse
import numpy as np
import pandas as pd
import time
import shutil
from PIL import Image
from tqdm import tqdm
import torch
import cv2
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torchvision.models as models

# 添加当前项目到环境变量
import sys
sys.path.append(os.path.join(os.getcwd(),"backend","api"))
from util import ProtestDatasetEvalFile, ProtestDatasetEvals, modified_resnet50
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class violence:
    def __init__(self, cuda):
        self = self
        self.path = os.getcwd()
        self.model_path = 'model_best.pth.tar'
        self.cuda = cuda
        print("*** loading model from {model}".format(model = self.model_path))
        self.model = modified_resnet50()
        if self.cuda:
            self.model = self.model.cuda()
        
        with open(os.path.join(self.path, 'backend' ,'api', self.model_path), 'rb') as f:
            self.model.load_state_dict(torch.load(f ,map_location='cpu')['state_dict'])

    def eval_one_file(self,img_path, model):
            """
            return model output of a images
            """
            model.eval()
            batch_size = 1
            workers = 0
            cuda = self.cuda
            timeout = 1
            # make dataloader
            try:

                dataset = ProtestDatasetEvalFile(img_path = img_path)
                data_loader = DataLoader(dataset,
                                        num_workers = workers,
                                        batch_size = batch_size,
                                        timeout= timeout)
                # load model

                outputs = []
                imgpaths = []

                n_imgs = 1
                with tqdm(total=n_imgs) as pbar:
                    for i, sample in enumerate(data_loader):
                        imgpath, input = sample['imgpath'], sample['image']
                        if cuda:
                            input = input.cuda()

                        input_var = Variable(input)
                        output = model(input_var)
                        outputs.append(output.cpu().data.numpy())
                        imgpaths = imgpath
                        if i < n_imgs / batch_size:
                            pbar.update(batch_size)
                        else:
                            pbar.update(n_imgs%batch_size)

                array = np.concatenate(outputs)
                return {
                    'protest': array[0][0],
                    'violence': array[0][1], 
                    'sign': array[0][2], 
                    'photo': array[0][3], 
                    'fire': array[0][4],
                    'police': array[0][5], 
                    'children': array[0][6], 
                    'group_20': array[0][7], 
                    'group_100': array[0][8], 
                    'flag': array[0][9],
                    'night': array[0][10], 
                    'shouting': array[0][11]
                }
            except:
                return {'protest': 0,'violence': 0}
    
    def eval_more_file(self,img_paths, model):
            """
            return model output of some images
            """
            print ("eval_more_file")
            model.eval()
            batch_size = len(img_paths)
            workers = 0
            cuda = self.cuda
            timeout = 1
            # make dataloader
            try:
                dataset = ProtestDatasetEvals(img_list = img_paths)
                print(dataset)
                data_loader = DataLoader(dataset,
                                        num_workers = workers,
                                        batch_size = batch_size,
                                        timeout= timeout)

                outputs = []
                imgpaths = []

                n_imgs = len(img_paths)
                with tqdm(total=n_imgs) as pbar:
                    for i, sample in enumerate(data_loader):
                        imgpath, input = sample['imgpath'], sample['image']
                        if cuda:
                            input = input.cuda()

                        input_var = Variable(input)
                        output = model(input_var)
                        outputs.append(output.cpu().data.numpy())
                        imgpaths = imgpath
                        if i < n_imgs / batch_size:
                            pbar.update(batch_size)
                        else:
                            pbar.update(n_imgs%batch_size)
                
                
                dataArr = []
                arrays = np.concatenate(outputs)
                # print (arrays)
                for array in arrays:
                    dataMap = {}
                    dataMap['protest'] = array[0]
                    dataMap['violence'] = array[1]
                    dataMap['sign'] = array[2]
                    dataMap['photo'] = array[3]
                    dataMap['fire'] = array[4]
                    dataMap['police'] = array[5]
                    dataMap['children'] = array[6]
                    dataMap['group_20'] = array[7]
                    dataMap['group_100'] = array[8]
                    dataMap['flag'] = array[9]
                    dataMap['night'] = array[10]
                    dataMap['shouting'] = array[11]
                    dataArr.append(dataMap)

                return {"result": dataArr}
            except:
                return {'protest': 0,'violence': 0}
                
    def check_violence(self,img_file):
        return self.eval_one_file(img_file, self.model)
    
    def check_violences(self,img_files):
        return self.eval_more_file(img_files, self.model)

if __name__ == '__main__':
    is_gpu = False
    img_file = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BDPAk8S.jpg")
    img_files = []
    
    img_file1 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","auW8xgi.jpg")
    img_file2 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bEu0Ihd.jpg")
    img_file3 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BgJGB9P.jpg")
    img_file4 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BGKV2Qg.jpg")
    img_file5 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bGpCUoU.jpg")
    img_file6 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bh2DK9Q.jpg")
    img_file7 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bhVEAOj.jpg")
    img_file8 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BIaBpE7.jpg")
    img_file9 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","Bid4Z0E.jpg")
    img_file10 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","biOwhIG.jpg")

    img_file11 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","auW8xgi.jpg")
    img_file12 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bEu0Ihd.jpg")
    img_file13 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BgJGB9P.jpg")
    img_file14 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BGKV2Qg.jpg")
    img_file15 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bGpCUoU.jpg")
    img_file16 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bh2DK9Q.jpg")
    img_file17 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","bhVEAOj.jpg")
    img_file18 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BIaBpE7.jpg")
    img_file19 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","Bid4Z0E.jpg")
    img_file20 = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","biOwhIG.jpg")
    
    img_files.append(img_file1)
    img_files.append(img_file2)
    img_files.append(img_file3)
    img_files.append(img_file4)
    img_files.append(img_file5)
    img_files.append(img_file6)
    img_files.append(img_file7)
    img_files.append(img_file8)
    img_files.append(img_file9)
    img_files.append(img_file10)
    img_files.append(img_file11)
    img_files.append(img_file12)
    img_files.append(img_file13)
    img_files.append(img_file14)
    img_files.append(img_file15)
    img_files.append(img_file16)
    img_files.append(img_file17)
    img_files.append(img_file18)
    img_files.append(img_file19)
    img_files.append(img_file20)

    myviolence = violence(is_gpu)
    t = time.time()
    startTime = int(round(t * 1000))
    # result = myviolence.check_violence(img_file)
    result = myviolence.check_violences(img_files)
    t = time.time()
    endTime = int(round(t * 1000))
    print("cost:"+ str(endTime - startTime) + "ms")
    print (result)
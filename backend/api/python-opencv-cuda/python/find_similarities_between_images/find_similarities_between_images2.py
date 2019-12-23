from skimage.measure import compare_ssim
import cv2
import os
import numpy as np
import re
import time

def compare_image(img1, img2, useCuda = False):
    #grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    #(score, diff) = compare_ssim(grayA, grayB, full=True)
    #print("SSIM: {}".format(score))

    original = img1
    image_to_compare = img2
    # print (original)
    # print (image_to_compare)

    # 1) Check if 2 images are equals
    if original.shape == image_to_compare.shape:
        #print("The images have same size and channels")
        if useCuda:
            difference = cv2.cuda.subtract(original, image_to_compare)
            b, g, r = cv2.split(difference)
            if cv2.cuda.countNonZero(b) == 0 and cv2.cuda.countNonZero(g) == 0 and cv2.cuda.countNonZero(r) == 0:
                #print("The images are completely Equal")
                pass
            else:
                pass
                #print("The images are NOT equal")
        else:
            difference = cv2.subtract(original, image_to_compare)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                #print("The images are completely Equal")
                pass
            else:
                pass
                #print("The images are NOT equal")

    # 2) Check for similarities between the 2 images

    # sift = cv2.xfeatures2d.SIFT_create()
    # surf = cv2.xfeatures2d.SURF_create()
    orb = cv2.ORB_create(nfeatures=1500)

    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    image_to_compare = cv2.cvtColor(image_to_compare, cv2.COLOR_BGR2GRAY)

    # kp_1, desc_1 = sift.detectAndCompute(original, None)
    # kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

    kp_1, desc_1 = orb.detectAndCompute(original, None)
    kp_2, desc_2 = orb.detectAndCompute(image_to_compare, None)

    # kp_1, desc_1 = surf.detectAndCompute(original, None)
    # kp_2, desc_2 = surf.detectAndCompute(image_to_compare, None)

    # index_params = dict(algorithm=0, trees=5)
    # search_params = dict()
    # flann = cv2.FlannBasedMatcher(index_params, search_params)

    # matches = flann.knnMatch(desc_1, desc_2, k=2)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc_1,desc_2)

    good_points = []
    ratio = 0.75
    # for m, n in matches:
    #     if m.distance < ratio*n.distance:
    #         good_points.append(m)

    for index, item in enumerate(matches):
        if index + 1 < len(matches) and matches[index].distance < ratio*matches[index + 1].distance:
            next_item = matches[index]
            good_points.append(next_item)

    return len(good_points)
    
array_img_list = [] 
def read_directory(directory_name, useCuda):
    array_img_list = os.listdir(directory_name)
    array_img_list.sort(key = lambda x:int(re.match(r'(\d+)',x).group()))
    check_img_list = []
    img1 = None
    img2 = None
    flag = True

    t = time.time()
    startTime = int(round(t * 1000))

    for index,fileName in enumerate(array_img_list):
        if len(check_img_list)==0:
            img1 = cv2.imread(directory_name + "/" + array_img_list[index])
        else:
            img1 = cv2.imread(directory_name + "/" + check_img_list[len(check_img_list)-1])
        if(index<len(array_img_list)-1):
            img2 = cv2.imread(directory_name + "/" + array_img_list[index+1])
            score = compare_image(img1,img2, useCuda)
            # print (index, score)

            if score<=120:
                if len(check_img_list)==0:
                    check_img_list.append(array_img_list[index])
                    check_img_list.append(array_img_list[index+1])   
                else:
                    check_img_list.append(array_img_list[index+1])
                flag = not flag
            else:
                if len(check_img_list)==0:
                    check_img_list.append(array_img_list[index])
    
    print(len(check_img_list))
    print(check_img_list)
    t = time.time()
    endTime = int(round(t * 1000))
    print ("Compare image time: ", endTime - startTime, "ms")            
            
if __name__ == '__main__':
    t = time.time()
    startTime = int(round(t * 1000))
    # read_directory(r'/home/nhydev/images2')
    # read_directory(r'/var/www/gallery/media/videos/capture_out_images/7320820e-1bc0-11ea-bffa-408d5c891351')
    # read_directory(r'/var/www/gallery/media/videos/capture_out_images/4eb31532-1bd2-11ea-bffa-408d5c891351')
    useCuda = False
    read_directory(r'/var/www/gallery/media/videos/capture_out_images/b5ce827c-17f6-11ea-bffa-408d5c891351', useCuda)
    t = time.time()
    endTime = int(round(t * 1000))
    print ("Total time: ", endTime - startTime, "ms")
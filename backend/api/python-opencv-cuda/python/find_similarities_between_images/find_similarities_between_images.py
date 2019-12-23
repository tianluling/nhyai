import cv2
import numpy as np
import time
import os

# cv2.ocl.setUseOpenCL(True)
# os.environ["CUDA_VISIBLE_DEVICES"] = '0'

# print (os.path.join(os.getcwd(),'original_golden_bridge.jpg'))
t = time.time()
startTime = int(round(t * 1000))

# original = cv2.imread(os.path.join(os.getcwd(),'backend','api','python-opencv-cuda','python','find_similarities_between_images','images','black_and_white.jpg'))
# image_to_compare = cv2.imread(os.path.join(os.getcwd(),'backend','api','python-opencv-cuda','python','find_similarities_between_images','images','blurred.jpg'))

original = cv2.imread("/var/www/gallery/media/videos/capture_out_images/b5ce827c-17f6-11ea-bffa-408d5c891351/101.jpg")
image_to_compare = cv2.imread("/var/www/gallery/media/videos/capture_out_images/b5ce827c-17f6-11ea-bffa-408d5c891351/103.jpg")

# print (original)
# print (image_to_compare)
# 1) Check if 2 images are equals
# print (original.shape)
if original.shape == image_to_compare.shape:
    print("The images have same size and channels")
    difference = cv2.subtract(original, image_to_compare)
    # difference = cv2.cuda.subtract(original, image_to_compare)
    b, g, r = cv2.split(difference)
    # b, g, r = cv2.cuda.split(difference)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
    # if cv2.cuda.countNonZero(b) == 0 and cv2.cuda.countNonZero(g) == 0 and cv2.cuda.countNonZero(r) == 0:
        print("The images are completely Equal")
    else:
        print("The images are NOT equal")
		
# 2) Check for similarities between the 2 images
# sift = cv2.xfeatures2d.SIFT_create()
# min_hessian = 400
# surf = cv2.xfeatures2d.SURF_create(min_hessian)
orb = cv2.ORB_create(nfeatures=1500)


# kp_1, desc_1 = sift.detectAndCompute(original, None)
# kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
image_to_compare = cv2.cvtColor(image_to_compare, cv2.COLOR_BGR2GRAY)

# kp_1, desc_1 = surf.detectAndCompute(original, None)
# kp_2, desc_2 = surf.detectAndCompute(image_to_compare, None)

kp_1, desc_1 = orb.detectAndCompute(original, None)
kp_2, desc_2 = orb.detectAndCompute(image_to_compare, None)

#print (kp_1)
#print (desc_1)
#print (kp_2)
#print (desc_2)

# SIFT way
# index_params = dict(algorithm=0, trees=5)
# search_params = dict()
# flann = cv2.FlannBasedMatcher(index_params, search_params)

# SURF way
# flann = cv2.FlannBasedMatcher()
# matches = flann.knnMatch(desc_1, desc_2, k=2)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(desc_1,desc_2)
good_points = []
ratio = 0.75

# SIFT and SURF way
# for m, n in matches:
# 	if m.distance < ratio*n.distance:
# 		good_points.append(m)

# ORB way
for index, item in enumerate(matches):
    # print (item.distance)
    if index + 1 < len(matches) and matches[index].distance < ratio*matches[index + 1].distance:
        next_item = matches[index]
        good_points.append(next_item)

print(len(good_points))
t = time.time()
endTime = int(round(t * 1000))
print ("time: ", endTime - startTime, "ms")
# result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
# cv2.imshow("result", result)

#cv2.imshow("Original", original)
#cv2.imshow("Duplicate", image_to_compare)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
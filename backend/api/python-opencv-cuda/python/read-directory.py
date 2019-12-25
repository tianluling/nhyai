import common as cm
import cv2

if __name__ == '__main__':
    original = cv2.imread("/home/nhydev/github/ai/nhyai/backend/api/python-opencv-cuda/python/find_similarities_between_images/images/black_and_white.jpg")
    image_to_compare = cv2.imread("/home/nhydev/github/ai/nhyai/backend/api/python-opencv-cuda/python/find_similarities_between_images/images/blurred.jpg")

    path = "/var/www/gallery/media/videos/capture_out_images/7320820e-1bc0-11ea-bffa-408d5c891351/*.jpg"
    useCuda = True
    ratio=0.75

    good_matcher_cpu = cm.cpuFindSimilaritiesBetweenImages(original, image_to_compare, ratio + 0.01)
    print("good_matcher with cpu: ",good_matcher_cpu)

    good_matcher_gpu = cm.gpuFindSimilaritiesBetweenImages(original, image_to_compare, ratio)
    print("good_matcher with gpu: ",good_matcher_gpu)

    check_img_list = cm.readDirectory(path, useCuda, ratio)
    print (check_img_list)
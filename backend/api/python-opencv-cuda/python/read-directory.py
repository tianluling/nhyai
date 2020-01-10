import common as cm
import cv2

if __name__ == '__main__':
    original = cv2.imread("/var/www/gallery/media/videos/capture_out_images/19b9c106-3134-11ea-bf2d-408d5c891351/103.jpg")
    image_to_compare = cv2.imread("/var/www/gallery/media/videos/capture_out_images/19b9c106-3134-11ea-bf2d-408d5c891351/104.jpg")

    path = "/var/www/gallery/media/videos/capture_out_images/19b9c106-3134-11ea-bf2d-408d5c891351/*.jpg"
    useCuda = True
    ratio=0.8

    good_matcher_cpu = cm.cpuFindSimilaritiesBetweenImages(original, image_to_compare, ratio + 0.01)
    print("good_matcher with cpu: ",good_matcher_cpu)

    good_matcher_gpu = cm.gpuFindSimilaritiesBetweenImages(original, image_to_compare, ratio)
    print("good_matcher with gpu: ",good_matcher_gpu)

    check_img_list = cm.readDirectory(path, useCuda, ratio,120)
    print (check_img_list)
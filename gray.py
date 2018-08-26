import os
import shutil
import cv2
import numpy as np
import aircv as ac
from xml.dom.minidom import parse
import xml.dom.minidom


def gray_scale(img):
    gray_img = img
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = (int(img[i, j][0]) + int(img[i, j][1]) + int(img[i, j][2]))/3
    return gray_img


def image_preprocess(image_dir, crop_dir):

    if not os.path.exists(crop_dir):
        os.mkdir(crop_dir)

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            img = cv2.imread(os.path.join(image_dir, file))
            img = gray_scale(img)
            cv2.imshow("gray", img)
            cv2.imwrite(os.path.join(crop_dir, "gray_" + file), img)


def main():

    data_dir = "C:/Users/lenovo/Desktop/train_data/A1"
    crop_dir = "gray_test"

    if os.path.exists(crop_dir):
        shutil.rmtree(crop_dir)
    os.mkdir(crop_dir)
    image_preprocess(data_dir, crop_dir)
    #for root, dirs, files in os.walk(data_dir):
        #for dir in dirs:
            #image_dir = os.path.join(root, dir)
            #image_preprocess(image_dir, os.path.join(crop_dir, dir))


if __name__ == '__main__':
    main()

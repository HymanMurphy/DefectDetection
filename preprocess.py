import os
import shutil
from PIL import Image

from xml.dom.minidom import parse
import xml.dom.minidom


def image_preprocess(xml_dir, image_dir, crop_dir):

    for root, dirs, files in os.walk(xml_dir):
        for file in files:
            DOMTree = xml.dom.minidom.parse(os.path.join(root, file))
            collection = DOMTree.documentElement
            defects = collection.getElementsByTagName("object")

            portion = os.path.splitext(file)
            print(portion[0])
            image_name = portion[0] + ".jpg"
            for defect in defects:
                name = defect.getElementsByTagName('name')[0].childNodes[0].data
                type = name[:name.find('_')]
                bndbox = defect.getElementsByTagName('bndbox')[0]
                xmin = int(bndbox.getElementsByTagName('xmin')[0].childNodes[0].data)
                ymin = int(bndbox.getElementsByTagName('ymin')[0].childNodes[0].data)
                xmax = int(bndbox.getElementsByTagName('xmax')[0].childNodes[0].data)
                ymax = int(bndbox.getElementsByTagName('ymax')[0].childNodes[0].data)
                xmid = int((xmin + xmax)/2)
                ymid = int((ymin + ymax)/2)
                box = (max(xmid - 500, 0), ymid - 500, xmid + 500, ymid + 500)
                image = Image.open(os.path.join(image_dir, image_name))
                crop_img = image.crop(box)
                if not os.path.exists(os.path.join(crop_dir, type)):
                    os.mkdir(os.path.join(crop_dir, type))
                crop_img.save(os.path.join(crop_dir, type, image_name))


def image_restore(image_dir, crop_dir):

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            image = Image.open(os.path.join(image_dir, file))
            type = file[:13]
            if not os.path.exists(os.path.join(crop_dir, type)):
                os.mkdir(os.path.join(crop_dir, type))
            image.save(os.path.join(crop_dir, type, file))


def main():
    data_dir = "D:/PCP/04ad16730a0-b"
    crop_dir = "D:/image_preprocess"

    if os.path.exists(crop_dir):
        shutil.rmtree(crop_dir)
    os.mkdir(crop_dir)

    for root, dirs, files in os.walk(data_dir):
        for dir in dirs:
            if dir.find("store") > 0:
                xml_dir = os.path.join(root, dir)
                image_dir = xml_dir.replace("store", "ng")
                # image_restore(image_dir, crop_dir)
                image_preprocess(xml_dir, image_dir, crop_dir)


if __name__ == '__main__':
    main()

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
            size = collection.getElementsByTagName('size')[0]
            width = int(size.getElementsByTagName('width')[0].childNodes[0].data)
            height = int(size.getElementsByTagName('height')[0].childNodes[0].data)
            defects = collection.getElementsByTagName('object')

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
                box_1 = (max(xmid - 75, 0), max(ymid - 75, 0), min(xmid + 25, width), min(ymid + 25, height))
                box_2 = (max(xmid - 75, 0), max(ymid - 25, 0), min(xmid + 25, width), min(ymid + 75, height))
                box_3 = (max(xmid - 25, 0), max(ymid - 75, 0), min(xmid + 75, width), min(ymid + 25, height))
                box_4 = (max(xmid - 75, 0), max(ymid - 25, 0), min(xmid + 25, width), min(ymid + 75, height))
                box_5 = (max(xmid - 50, 0), max(ymid - 50, 0), min(xmid + 50, width), min(ymid + 50, height))
                box = [box_1, box_2, box_3, box_4, box_5]
                image = Image.open(os.path.join(image_dir, image_name))
                """
                for i in range(5):
                    crop_img = image.crop(box[i])
                    if not os.path.exists(os.path.join(crop_dir, type)):
                        os.mkdir(os.path.join(crop_dir, type))
                    crop_img.save(os.path.join(crop_dir, type, str(i) + '_' + image_name))
                """
                box_normal_1 = (max(xmid - 50, 0), min(ymid + 400, height), min(xmid + 50, width), min(ymid + 500, height))
                box_normal_2 = (min(xmid + 200, width), max(ymid - 50, 0), min(xmid + 300, width), min(ymid + 50, height))
                box_normal_3 = (min(xmid + 200, width), min(ymid + 400, height), min(xmid + 300, width), min(ymid + 500, height))
                box_normal_4 = (max(xmid - 400, 0), max(ymid - 50, 0), max(xmid - 300, 0), min(ymid + 50, height))
                box_normal_5 = (max(xmid - 50, 0), max(ymid - 500, 0), min(xmid + 50, width), max(ymid - 400, 0))
                box_normal_6 = (max(xmid - 400, 0), max(ymid - 500, 0), max(xmid - 300, 0), max(ymid - 400, 0))
                box_normal = [box_normal_1, box_normal_2, box_normal_3, box_normal_4, box_normal_5, box_normal_6]
                for i in range(6):
                    crop_img = image.crop(box_normal[i])
                    if not os.path.exists(os.path.join(crop_dir, "normal")):
                        os.mkdir(os.path.join(crop_dir, "normal"))
                    crop_img.save(os.path.join(crop_dir, "normal", str(i) + '_' + image_name))


def image_restore(image_dir, crop_dir):

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            image = Image.open(os.path.join(image_dir, file))
            type = file[:13]
            if not os.path.exists(os.path.join(crop_dir, type)):
                os.mkdir(os.path.join(crop_dir, type))
            image.save(os.path.join(crop_dir, type, file))


def image_reprocess(image_dir, dir, repro_dir):

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            image = Image.open(os.path.join(image_dir, file))
            image_resize = image.resize((128, 128))
            image_rotate = image.rotate(135)
            image_trans1 = image.transpose(Image.FLIP_LEFT_RIGHT)
            image_trans2 = image.transpose(Image.FLIP_TOP_BOTTOM)

            if not os.path.exists(os.path.join(repro_dir, dir)):
                os.mkdir(os.path.join(repro_dir, dir))
            image_resize.save(os.path.join(repro_dir, dir, "rs_" + file))
            image_rotate.save(os.path.join(repro_dir, dir, "ro_" + file))
            image_trans1.save(os.path.join(repro_dir, dir, "tr1_" + file))
            image_trans2.save(os.path.join(repro_dir, dir, "tr2_" + file))


def main():

    #image_dir = "D:/train_img"
    #repro_dir = "D:/repro_img"
    #if os.path.exists(repro_dir):
        #shutil.rmtree(repro_dir)
    #os.mkdir(repro_dir)
    """
    for root, dirs, files in os.walk(image_dir):
        for dir in dirs:
            if dir.find("A") > -1:
                image_dir = os.path.join(root, dir)
                image_reprocess(image_dir, dir, repro_dir)
    """
    data_dir = "D:/PCP/04ad16730a0-b"
    crop_dir = "D:/train_img"

    #if os.path.exists(crop_dir):
        #shutil.rmtree(crop_dir)
    #os.mkdir(crop_dir)

    for root, dirs, files in os.walk(data_dir):
        for dir in dirs:
            if dir.find("store") > 0:
                xml_dir = os.path.join(root, dir)
                image_dir = xml_dir.replace("store", "ng")
                # image_restore(image_dir, crop_dir)
                image_preprocess(xml_dir, image_dir, crop_dir)

if __name__ == '__main__':
    main()

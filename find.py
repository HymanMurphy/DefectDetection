import cv2
import aircv as ac


def draw_rectangle(img, pos, h, w, color, line_width):
    cv2.rectangle(img, (int(pos[0] - w/2), int(pos[1] - h/2)), (int(pos[0] + w/2), int(pos[1] + h/2)), color, line_width)


def main():
    #imgsrc = cv2.imread("D:/PCP/04ad16730a0-b/04ad16730a0-b-ng/04ad16730a0-b-2.jpg")
    imgsrc = cv2.imread("C:/Users/lenovo/Pictures/Saved Pictures/part1.jpg")
    imgsrc2 = cv2.imread("C:/Users/lenovo/Pictures/Saved Pictures/part2.jpg")
    #imgobj = cv2.imread("C:/Users/lenovo/Desktop/train_data/A1/04ad16730a0-b-30.jpg")
    imgobj = cv2.imread("C:/Users/lenovo/Pictures/Saved Pictures/04ad16730a0-b-1 (4).jpg")


    size = imgsrc.shape
    h = size[0]
    w = size[1]
    scale = 480/h
    th, tw = h*scale, w*scale

    pos_list = ac.find_all_template(imgsrc, imgobj)
    pos_list2 = ac.find_all_template(imgsrc2, imgobj)
    print(pos_list)
    print(pos_list2)
    color = (0, 255, 0)
    line_width = 10
    for pos in pos_list:
        conf = pos['confidence']
        pos = pos['result']

        if conf < 0.9:
            continue
        draw_rectangle(imgsrc, pos, imgobj.shape[0], imgobj.shape[1], color, line_width)
    cv2.namedWindow("Detection", 0)
    cv2.resizeWindow("Detection", int(tw), int(th))
    cv2.imshow('Detection', imgsrc)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
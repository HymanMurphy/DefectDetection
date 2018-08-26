import cv2
import random
import numpy as np
import random


image_shape = (128, 128)


def scale(img, size):
    s = size / min(img.shape[0], img.shape[1])
    h, w = int(round(img.shape[0] * s)), int(round(img.shape[1] * s))
    return cv2.resize(img, (w, h))


def center_crop(img, shape):
    h, w = img.shape[:2]
    sx, sy = (w - shape[1]) // 2, (h - shape[0]) // 2
    img = img[sy:sy + shape[0], sx:sx + shape[1]]
    return img


def random_size_crop(img):
    NR_REPEAT = 10

    h, w = img.shape[:2]
    area = h * w
    ar = [3./4, 4./3]
    for i in range(NR_REPEAT):
        target_area = random.uniform(0.08, 1.0) * area
        target_ar = random.choice(ar)
        nw = int(round((target_area * target_ar) ** 0.5))
        nh = int(round((target_area / target_ar) ** 0.5))

        if random.rand() < 0.5:
            nh, nw = nw, nh

        if nh <= h and nw <= w:
            sx, sy = random.randint(w - nw + 1), random.randint(h - nh + 1)
            img = img[sy:sy + nh, sx:sx + nw]

            return cv2.resize(img, image_shape[::-1])

    size = min(image_shape[0], image_shape[1])
    return center_crop(scale(img, size), image_shape)


def grayscale(img):
    w = np.array([0.114, 0.587, 0.299]).reshape(1, 1, 3)
    gs = np.zeros(img.shape[:2])
    gs = (img * w).sum(axis=2, keepdims=True)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = gs[i, j]
    return img


def brightness_aug(img, val):
    alpha = 1. + val * (random.random() * 2 - 1)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = img[i, j] * alpha

    return img


def contrast_aug(img, val):
    gs = grayscale(img)
    gs = gs.mean()
    alpha = 1. + val * (random.random() * 2 - 1)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = img[i, j] * alpha + gs * (1 - alpha)

    return img


def saturation_aug(img, val):
    gs = grayscale(img)
    print(gs.shape)
    alpha = 1. + val * (random.random() * 2 - 1)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = img[i, j] * alpha + gs[i, j] * (1 - alpha)

    return img


def color_jitter(img, brightness, contrast, saturation):
    augs = [(brightness_aug, brightness),
            (contrast_aug, contrast),
            (saturation_aug, saturation)]
    random.shuffle(augs)

    for aug, val in augs:
        img = aug(img, val)

    return img


def lighting(img, std):
    eigval = np.array([ 0.2175, 0.0188, 0.0045 ])
    eigvec = np.array([
        [ -0.5836, -0.6948,  0.4203 ],
        [ -0.5808, -0.0045, -0.8140 ],
        [ -0.5675, 0.7192, 0.4009],
    ])
    if std == 0:
        return img

    alpha = random.randint(3) * std
    bgr = eigvec * alpha.reshape(1, 3) * eigval.reshape(1, 3)
    bgr = bgr.sum(axis=1).reshape(1, 1, 3)
    img = img + bgr

    return img


def horizontal_flip(img, prob):
    if random.random() < prob:
        return img[:, ::-1]
    return img


def equalization(img):
    max = np.max(img)
    min = np.min(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j] = int(255.0*(img[i,j]-min)/(max-min))
    return img


def gray2binary(img):
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return img


def minus(img1, img2):
    minus_img = img1.copy()
    for i in range(minus_img.shape[0]):
        for j in range(minus_img.shape[1]):
            if (minus_img[i,j] - img2[i,j]).all():
                minus_img[i,j] = 255
            else:
                minus_img[i,j] = 0
    return minus_img


def main():
    img = cv2.imread("C:/Users/lenovo/Desktop/train_data/A1/04ad16730a0-b-176.jpg",0)
    img2 = cv2.imread("C:/Users/lenovo/Pictures/Saved Pictures/part3.jpg",0)
    #img = np.array(cv2.imread("C:/Users/lenovo/Desktop/train_data/A1/04ad16730a0-b-12.jpg"))
    #img2 = np.array(cv2.imread("C:/Users/lenovo/Desktop/train_data/A1/04ad16730a0-b-12.jpg"))
    #cv2.imshow("img2", img2)
    equal_img = equalization(img)
    binary_img = gray2binary(equal_img)
    cv2.imshow("img", binary_img)

    equal_img2 = equalization(img2)
    binary_img2 = gray2binary(equal_img2)
    #cv2.imshow("img2", binary_img2)

    #minus_img = minus(binary_img2, binary_img)

    #cv2.imshow("minus", minus_img)
    '''
    temp = img
    temp = grayscale(temp)
    cv2.imshow("gray", img)
    img = temp
    img = brightness_aug(img, 0.9)
    cv2.imshow("brightness", img)
    img = temp
    img = contrast_aug(img, 0.9)
    cv2.imshow("contrast", img)
    img = temp
    img = saturation_aug(img, 0.9)
    cv2.imshow("saturation", img)
    '''
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
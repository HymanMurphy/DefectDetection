import cv2
import matplotlib.pyplot as plt

img = cv2.imread('test/04ad16730a0-t-15.jpg', 0)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2) #换行符号 \
#th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) #换行符号 \
images = [img,th1]
plt.figure()
for i in range(2):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')

plt.show()


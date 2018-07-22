from PIL import Image, ImageFilter
img = Image.open("image_retraining/data/1.jpg")
L = img.convert('L')
L = img.convert('1')
im_contour = img.filter(ImageFilter.CONTOUR)
im_contour.show()
L.show()
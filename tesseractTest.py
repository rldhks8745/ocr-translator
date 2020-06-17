import cv2
import pytesseract

print("version: "+ pytesseract.get_tesseract_version().vstring)

gray = cv2.imread('test5.png', cv2.IMREAD_GRAYSCALE)
gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
# cv2.imshow('gray', gray)
#
(thresh, im_bw1) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
cv2.imshow('im_bw1', im_bw1)

blur1 = cv2.GaussianBlur(im_bw1, (3, 3), 0)
cv2.imshow('blur1', blur1)
(thresh, im_bw2) = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
cv2.imshow('im_bw2', im_bw2)

blur2 = cv2.GaussianBlur(im_bw1, (5, 5), 0)
cv2.imshow('blur2', blur2)
(thresh, im_bw3) = cv2.threshold(blur2, 127, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
cv2.imshow('im_bw3', im_bw3)


# im_mean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)
# cv2.imshow('im_mean', im_mean)
# im_mean2 = cv2.adaptiveThreshold(im_mean, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 2)
# cv2.imshow('im_mean2', im_mean2)
# im_ga = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)
# cv2.imshow('im_ga', im_ga)


text = pytesseract.image_to_string(im_bw1, config='--tessdata-dir "tessdata" -l eng --oem 3 --psm 3')
print("\n im_bw>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n", text)
text = pytesseract.image_to_string(im_bw2, config='--tessdata-dir "tessdata" -l eng --oem 3 --psm 3')
print("\n im_bw2>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n", text)
text = pytesseract.image_to_string(im_bw3, config='--tessdata-dir "tessdata" -l eng --oem 3 --psm 3')
print("\n im_bw3>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n", text)

cv2.waitKey(0)
cv2.destroyAllWindows()


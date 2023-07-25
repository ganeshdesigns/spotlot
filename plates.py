import cv2 as cv
import numpy as np
import sys
import pytesseract
from pickle import NONE

capture = cv.VideoCapture(0)
pytesseract.pytesseract.tesseract_cmd =r'D:/Programs/Code Palette/Tesseract/tesseract.exe'

def segment_characters(image):
    img_lp = cv.resize(image, (333, 75))
    img_gray_lp = cv.cvtColor(img_lp, cv.COLOR_BGR2GRAY)
    _, img_binary_lp = cv.threshold(
        img_gray_lp, 200, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    img_binary_lp = cv.erode(img_binary_lp, (3, 3))
    img_binary_lp = cv.dilate(img_binary_lp, (3, 3))
    LP_WIDTH = img_binary_lp.shape[0]
    LP_HEIGHT = img_binary_lp.shape[1]
    img_binary_lp[0:3, :] = 255
    img_binary_lp[:, 0:3] = 255
    img_binary_lp[72:75, :] = 255
    img_binary_lp[:, 330:333] = 255
    dimensions = [LP_WIDTH/6,
                  LP_WIDTH/2,
                  LP_HEIGHT/10,
                  2*LP_HEIGHT/3]
    rev = pytesseract.image_to_string(img_binary_lp)
    if(len(rev) > 10):
        for i in range(len(rev)):
            if(rev[i].isalnum() or rev[i] == ' '):
                carnumber = str(rev[i])
                print(carnumber, end='')
        sys.exit(0)

def preprocess(img):
    blur = cv.GaussianBlur(img, (7, 7), 0)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    sobelx = cv.Sobel(gray, cv.CV_8U, 1, 0, ksize=3)
    ret2, otsu_thresh = cv.threshold(
        sobelx, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    element = cv.getStructuringElement(cv.MORPH_RECT, (22, 5))
    morph_n_thresh = cv.morphologyEx(otsu_thresh, cv.MORPH_CLOSE, element)
    return morph_n_thresh

def extract_contours(after_preprocess):
    contours, _ = cv.findContours(
        after_preprocess, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours

def ratioCheck(area, width, height):
    min = 4500
    max = 30000
    ratioMin = 3
    ratioMax = 6
    ratio = float(width) / float(height)
    if ratio < 1:
        ratio = 1 / ratio
    if (area < min or area > max) or (ratio < ratioMin or ratio > ratioMax):
        return False
    return True

def clean_plate(plate):
    gray = cv.cvtColor(plate, cv.COLOR_BGR2GRAY)
    thresh = cv.adaptiveThreshold(
        gray,  255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    contours, _ = cv.findContours(
        thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if contours:
        areas = []
        for c in contours:
            areas.append(cv.contourArea(c))
        max_index = np.argmax(areas)
        max_cnt = contours[max_index]
        max_cntArea = areas[max_index]
        x, y, w, h = cv.boundingRect(max_cnt)
        rect = cv.minAreaRect(max_cnt)
        if not ratioCheck(max_cntArea, plate.shape[1],
                          plate.shape[0]):
            return plate, False, None
        return plate, True, [x, y, w, h]
    else:
        return plate, False, None

def check_plate(img, cnts):
    min_rect = cv.minAreaRect(cnts)
    if validateRatio(min_rect):
        x, y, w, h = cv.boundingRect(cnts)
        after_validation_img = img[y:y+h, x:x+w]
        if(after_validation_img.shape[1] > after_validation_img.shape[0]):
            after_clean_plate_img, plateFound, coordinates = clean_plate(
                after_validation_img)
            if plateFound:
                for c in cnts:
                    peri = cv.arcLength(c, True)
                    approx = cv.approxPolyDP(c, 0.20 * peri, True)
                    screenCnt = 0
                    if len(approx) == 4:
                        screenCnt = approx
                        break
                    if screenCnt is not NONE:
                        char = segment_characters(after_clean_plate_img)
    return None, None, None

def find_possible_plate(img):
    plates = []
    char_on_plate = []
    corresponding_area = []
    after_preprocess = preprocess(img)
    possible_plate_contours = extract_contours(
        after_preprocess)
    for cnts in possible_plate_contours:
        plate, characters_on_plate, coordinates = check_plate(img, cnts)
        if plate is not None:
            plates.append(plate)
            char_on_plate.append(characters_on_plate)
            corresponding_area.append(coordinates)

def preRatioCheck(area, width, height):
    min = 4500
    max = 30000
    ratioMin = 2.5
    ratioMax = 7
    ratio = float(width)/float(height)
    if ratio < 1:
        ratio = 1/ratio
    if (area < min or area > max) or (ratio < ratioMin or ratio > ratioMax):
        return False
    return True

def validateRatio(min_rect):
    (x, y), (w, h), rect_angle = min_rect
    if(w > h):
        angle = -rect_angle
    else:
        angle = rect_angle+90
    if(angle > 15):
        return False
    if(h == 0 or w == 0):
        return False
    area = w*h
    if not preRatioCheck(area, w, h):
        return False
    else:
        return True

class platesmap:
    def main():
        count = 1
        start_frame_number = 0
        while True:
            ret, frame = capture.read()
            if ret:
                cv.imshow('original video', frame)
                find_possible_plate(frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            capture.set(cv.CAP_PROP_POS_FRAMES, start_frame_number)
            start_frame_number += 11

if __name__ == '__main__':
    platesmap.main()

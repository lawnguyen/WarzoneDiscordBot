import pytesseract
import cv2
import sys
import time
import numpy as np
from PIL import Image
from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

def preprocess_image(im, width, height, left_ratio, top_ratio, right_ratio, bottom_ratio):
    RESIZE_FACTOR = 2
    IMAGE_CONVERSION_MODE = "LA"

    _crop_left = int(width * left_ratio)
    _crop_top = int(height * top_ratio)
    _crop_right = int(width * right_ratio)
    _crop_bottom = int(height * bottom_ratio)

    _cropped_im = im.crop((_crop_left, _crop_top, _crop_right, _crop_bottom))
    _cropped_im = _cropped_im.convert(IMAGE_CONVERSION_MODE)
    _larger_size = tuple(RESIZE_FACTOR * x for x in _cropped_im.size)
    _cropped_im = _cropped_im.resize(_larger_size, Image.ANTIALIAS)
    #_cropped_im.show()

    return _cropped_im


def main(display_number):
    # Get the rect of the display
    _display_rect = getDisplayRects()[display_number - 1]

    _im = getRectAsImage(_display_rect)
    _width, _height = _im.size

    # P1
    _p1_preprocessed_im = preprocess_image(_im, _width, _height, 0.034, 0.95, 0.08, 0.97)
    # P2
    _p2_preprocessed_im = preprocess_image(_im, _width, _height, 0.035, 0.88, 0.08, 0.9)
    # P3
    _p3_preprocessed_im = preprocess_image(_im, _width, _height, 0.035, 0.818, 0.08, 0.84)
    # P4
    _p4_preprocessed_im = preprocess_image(_im, _width, _height, 0.035, 0.818, 0.08, 0.84)

    pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\Lawrence\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
    print(pytesseract.image_to_string(_p1_preprocessed_im))
    print(pytesseract.image_to_string(_p2_preprocessed_im))
    print(pytesseract.image_to_string(_p3_preprocessed_im))
    print(pytesseract.image_to_string(_p4_preprocessed_im))


if __name__ == "__main__": 
    if (len(sys.argv) == 2):
        display_number = int(sys.argv[1])
    else:
        display_number = int(input("Display number that modern warfare is running on (e.g. 2): "))
        
    time.sleep(3)
    main(display_number)
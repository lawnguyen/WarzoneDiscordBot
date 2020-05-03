import pytesseract
import cv2
import sys
import time
import numpy as np
from PIL import Image
from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

def main(display_number):
    # Get the rect of the display
    _display_rect = getDisplayRects()[display_number - 1]

    _im = getRectAsImage(_display_rect)
    _width, _height = _im.size

    RESIZE_FACTOR = 2
    IMAGE_CONVERSION_MODE = "LA"

    # P1
    _p1_crop_left = int(_width * 0.034)
    _p1_crop_top = int(_height * 0.95)
    _p1_crop_right = int(_width * 0.08)
    _p1_crop_bottom = int(_height * 0.97)

    _p1_cropped_im = _im.crop((_p1_crop_left, _p1_crop_top, _p1_crop_right, _p1_crop_bottom))
    _p1_cropped_im = _p1_cropped_im.convert(IMAGE_CONVERSION_MODE)
    _larger_size = tuple(RESIZE_FACTOR * x for x in _p1_cropped_im.size)
    _p1_cropped_im = _p1_cropped_im.resize(_larger_size, Image.ANTIALIAS)
    #_p1_cropped_im.show()

    #P2
    _p2_crop_left = int(_width * 0.035)
    _p2_crop_top = int(_height * 0.88)
    _p2_crop_right = int(_width * 0.08)
    _p2_crop_bottom = int(_height * 0.9)

    _p2_cropped_im = _im.crop((_p2_crop_left, _p2_crop_top, _p2_crop_right, _p2_crop_bottom))
    _p2_cropped_im = _p2_cropped_im.convert(IMAGE_CONVERSION_MODE)
    _larger_size = tuple(RESIZE_FACTOR * x for x in _p2_cropped_im.size)
    _p2_cropped_im = _p2_cropped_im.resize(_larger_size, Image.ANTIALIAS)
    # _p2_cropped_im.show()

    #P3
    _p3_crop_left = int(_width * 0.035)
    _p3_crop_top = int(_height * 0.818)
    _p3_crop_right = int(_width * 0.08)
    _p3_crop_bottom = int(_height * 0.84)

    _p3_cropped_im = _im.crop((_p3_crop_left, _p3_crop_top, _p3_crop_right, _p3_crop_bottom))
    _p3_cropped_im = _p3_cropped_im.convert(IMAGE_CONVERSION_MODE)
    _larger_size = tuple(RESIZE_FACTOR * x for x in _p3_cropped_im.size)
    _p3_cropped_im = _p3_cropped_im.resize(_larger_size, Image.ANTIALIAS)
    # _p3_cropped_im.show()

    #P4
    _p4_crop_left = int(_width * 0.035)
    _p4_crop_top = int(_height * 0.818)
    _p4_crop_right = int(_width * 0.08)
    _p4_crop_bottom = int(_height * 0.84)

    _p4_cropped_im = _im.crop((_p4_crop_left, _p4_crop_top, _p4_crop_right, _p4_crop_bottom))
    _p4_cropped_im = _p4_cropped_im.convert(IMAGE_CONVERSION_MODE)
    _larger_size = tuple(RESIZE_FACTOR * x for x in _p4_cropped_im.size)
    _p4_cropped_im = _p4_cropped_im.resize(_larger_size, Image.ANTIALIAS)
    #_p4_cropped_im.show()


    # OCR
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\Lawrence\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
    print(pytesseract.image_to_string(_p1_cropped_im))
    print(pytesseract.image_to_string(_p2_cropped_im))
    print(pytesseract.image_to_string(_p3_cropped_im))
    #print(pytesseract.image_to_string(_p4_cropped_im))


if __name__ == "__main__": 
    if (len(sys.argv) == 2):
        display_number = int(sys.argv[1])
    else:
        display_number = int(input("Display number that modern warfare is running on (e.g. 2): "))

    main(display_number)
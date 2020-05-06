import pytesseract
import cv2
import sys
import time
import numpy as np
from PIL import Image
from datetime import date
from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

MODE = "0"

def preprocess_image(im, width, height, left_ratio, top_ratio, right_ratio, bottom_ratio, player):
    RESIZE_FACTOR = 3
    IMAGE_CONVERSION_MODE = "LA"

    # Crop image to bounding boxes
    _crop_left = int(width * left_ratio)
    _crop_top = int(height * top_ratio)
    _crop_right = int(width * right_ratio)
    _crop_bottom = int(height * bottom_ratio)

    _cropped_im = im.crop((_crop_left, _crop_top, _crop_right, _crop_bottom))

    # Resize
    _larger_size = tuple(RESIZE_FACTOR * x for x in _cropped_im.size)
    _cropped_im = _cropped_im.resize(_larger_size, Image.ANTIALIAS)

    # Convert to opencv consumable type, in grayscale
    _open_cv_im = cv2.cvtColor(np.array(_cropped_im), cv2.COLOR_RGB2GRAY)

    # Apply automatic Otsu thresholding
    #_, thr = cv2.threshold(_open_cv_im, 0, 255, cv2.THRESH_OTSU)

    if (MODE == "2" or MODE == player):
        cv2.imshow('win', _open_cv_im)     
        if cv2.waitKey(0) & 0xff == 27: 
            cv2.destroyAllWindows()

    return _open_cv_im


def main(display_number, iteration):
    # Get the rect of the display
    _display_rect = getDisplayRects()[display_number - 1]

    _im = getRectAsImage(_display_rect)
    _width, _height = _im.size

    _today = str(date.today())

    # P1
    _p1_preprocessed_im = preprocess_image(_im, _width, _height, 0.034, 0.95, 0.08, 0.965, "p1")
    # P2
    _p2_preprocessed_im = preprocess_image(_im, _width, _height, 0.035, 0.88, 0.08, 0.895, "p2")
    # P3
    _p3_preprocessed_im = preprocess_image(_im, _width, _height, 0.035, 0.818, 0.08, 0.84, "p3")
    # P4
    _p4_preprocessed_im = preprocess_image(_im, _width, _height, 0.035, 0.75, 0.08, 0.768, "p4")

    if (MODE == "1"):
        cv2.imwrite("{}-p1-{}.png".format(_today, iteration), _p1_preprocessed_im)
        cv2.imwrite("{}-p2-{}.png".format(_today, iteration), _p2_preprocessed_im)
        cv2.imwrite("{}-p3-{}.png".format(_today, iteration), _p3_preprocessed_im)
        cv2.imwrite("{}-p4-{}.png".format(_today, iteration), _p4_preprocessed_im)

    pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\Lawrence\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
    print("{} - p1 - iteration {}".format(_today, iteration))
    print(pytesseract.image_to_string(_p1_preprocessed_im))
    print("{} - p2 - iteration {}".format(_today, iteration))
    print(pytesseract.image_to_string(_p2_preprocessed_im))
    print("{} - p3 - iteration {}".format(_today, iteration))
    print(pytesseract.image_to_string(_p3_preprocessed_im))
    print("{} - p4 - iteration {}".format(_today, iteration))
    print(pytesseract.image_to_string(_p4_preprocessed_im))

def menu_choice():
    print("(0) - Only print statements")
    print("(1) - Write screenshots to file system")
    print("(2) - Show screenshots in photo viewer")
    print("(3) - Show screenshots for specific player")

    _choice = input("Select mode: ")

    if (_choice == "3"):
        _player_choice = int(input("Select player number (i.e. 3): "))

        _player_choices = {
            1: "p1",
            2: "p2",
            3: "p3",
            4: "p4"
        }
        return _player_choices.get(_player_choice)

    return _choice

if __name__ == "__main__": 
    if (len(sys.argv) == 2):
        _display_number = int(sys.argv[1])
    else:
        _display_number = int(input("Display number that modern warfare is running on (e.g. 2): "))

    MODE = menu_choice()
        
    time.sleep(10)
    _i = 0
    while (1):
        _i += 1
        main(_display_number, _i)
        time.sleep(30)
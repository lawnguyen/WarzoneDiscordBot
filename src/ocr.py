import pytesseract
import cv2
import sys
from PIL import Image
from desktopmagic.screengrab_win32 import (
    getScreenAsImage, getDisplayRects, getRectAsImage)

def main(display_number):
    # Get the rect of the display
    _display_rect = getDisplayRects()[display_number - 1]

    # Take and crop screenshot to the third quadrant
    im = getRectAsImage(_display_rect)
    width, height = im.size

    _crop_left = 0
    _crop_top = int(height / 2)
    _crop_right = int(width / 2)
    _crop_bottom = height

    cropped_im = im.crop((_crop_left, _crop_top, _crop_right, _crop_bottom))
    cropped_im.show()

    # template match

    # Ocr

# Save the entire virtual screen as a PNG
getScreenAsImage().save("../data/screenshot.png", format="png")




if __name__ == "__main__": 
    if (len(sys.argv) == 2):
        display_number = int(sys.argv[1])
    else:
        display_number = int(input("Display number that modern warfare is running on (e.g. 2): "))

    main(display_number)
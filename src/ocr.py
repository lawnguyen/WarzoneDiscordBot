import pytesseract
import cv2
import sys
from desktopmagic.screengrab_win32 import (
    getScreenAsImage, getDisplayRects, getRectAsImage)

def main(display_number):
    # Get the rect of the display
    _display_rect = getDisplayRects()[display_number - 1]

    # Get the third quarter region of display rect
    # rect points are relative to (0,0)
    _rect_left = _display_rect[0]
    _rect_top = _display_rect[1]
    _rect_right = _display_rect[2]
    _rect_bottom = _display_rect[3]

    _third_quadrant_rect = (
        _rect_left, 
        int(_rect_bottom / 2),
        int(_rect_left / 2),
        _rect_bottom)

    # Save a screenshot of the the lower left region of display
    getRectAsImage(_third_quadrant_rect).save("../data/screenshot.png", format="png")

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
import cv2
import numpy as np
import pytesseract
from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage
from PIL import Image
from datetime import date
from cropRatio import CropRatio

class Processor:
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\Lawrence\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"

    def __init__(self, display_number, mode):
        self._display_number = display_number
        self._display_rect = getDisplayRects()[self._display_number - 1]
        self._mode = mode

        self.buy_back_count = 0

    def is_game_started(self):
        im = getRectAsImage(self._display_rect)
        width, height = im.size

        # Check if game is started by detecting the word "Armistice" on screen
        # which shows on the screen at the beginning of the match before you drop
        armistice_crop_ratio = CropRatio(0.068, 0.720, 0.198, 0.761)
        preprocessed_im = self._preprocess_image(im, width, height, armistice_crop_ratio, "start")
        print(pytesseract.image_to_string(preprocessed_im, lang="eng", config="--psm 8 --oem 3"))

        return False
    
    def get_cash_total(self, iteration):
        im = getRectAsImage(self._display_rect)
        width, height = im.size

        today = str(date.today())

        # P1
        p1_crop_ratio = CropRatio(0.034, 0.95, 0.08, 0.965)
        p1_preprocessed_im = self._preprocess_image(im, width, height, p1_crop_ratio, "p1")
        # P2
        p2_crop_ratio = CropRatio(0.035, 0.88, 0.08, 0.895)
        p2_preprocessed_im = self._preprocess_image(im, width, height, p2_crop_ratio, "p2")
        # P3
        p3_crop_ratio = CropRatio(0.035, 0.818, 0.08, 0.84)
        p3_preprocessed_im = self._preprocess_image(im, width, height, p3_crop_ratio, "p3")
        # P4
        p4_crop_ratio = CropRatio(0.035, 0.75, 0.08, 0.768)
        p4_preprocessed_im = self._preprocess_image(im, width, height, p4_crop_ratio, "p4")

        if (self._mode == "1"):
            cv2.imwrite("{}-p1-{}.png".format(today, iteration), p1_preprocessed_im)
            cv2.imwrite("{}-p2-{}.png".format(today, iteration), p2_preprocessed_im)
            cv2.imwrite("{}-p3-{}.png".format(today, iteration), p3_preprocessed_im)
            cv2.imwrite("{}-p4-{}.png".format(today, iteration), p4_preprocessed_im)

        tess_config = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789$"

        p1_read = pytesseract.image_to_string(p1_preprocessed_im, lang = "eng", \
            config = tess_config)
        p2_read = pytesseract.image_to_string(p2_preprocessed_im, lang = "eng", \
            config = tess_config)
        p3_read = pytesseract.image_to_string(p3_preprocessed_im, lang = "eng", \
            config = tess_config)
        p4_read = pytesseract.image_to_string(p4_preprocessed_im, lang = "eng", \
            config = tess_config)

        print("{} - p1 - iteration {}".format(today, iteration))
        print(p1_read)
        print("{} - p2 - iteration {}".format(today, iteration))
        print(p2_read)
        print("{} - p3 - iteration {}".format(today, iteration))
        print(p3_read)
        print("{} - p4 - iteration {}".format(today, iteration))
        print(p4_read)

        # Reset buy_back_count so we can get a fresh value
        self.buy_back_count = 0
        
        total = (self._parse_read(p1_read) + self._parse_read(p2_read) + 
            self._parse_read(p3_read) + self._parse_read(p4_read))

        print("TOTAL: ")
        print(total)
        print()

        return total

    def _preprocess_image(self, im, width, height, crop_ratio, player):

        RESIZE_FACTOR = 3
        IMAGE_CONVERSION_MODE = "LA"

        # Crop image to bounding boxes
        crop_left = int(width * crop_ratio.left)
        crop_top = int(height * crop_ratio.top)
        crop_right = int(width * crop_ratio.right)
        crop_bottom = int(height * crop_ratio.bottom)

        cropped_im = im.crop((crop_left, crop_top, crop_right, crop_bottom))

        # Resize
        larger_size = tuple(RESIZE_FACTOR * x for x in cropped_im.size)
        cropped_im = cropped_im.resize(larger_size, Image.ANTIALIAS)

        # Convert to opencv consumable type, in grayscale
        open_cv_im = cv2.cvtColor(np.array(cropped_im), cv2.COLOR_RGB2GRAY)

        # Apply automatic Otsu thresholding
        _, thr = cv2.threshold(open_cv_im, 0, 255, cv2.THRESH_OTSU)

        # Invert image
        inverted_im = cv2.bitwise_not(thr)

        if (self._mode == "2" or self._mode == player):
            cv2.imshow("win", inverted_im)  
            if cv2.waitKey(0) & 0xff == 27:
                cv2.destroyAllWindows()

        return inverted_im

    def _parse_read(self, str):
        # Remove all whitespace
        str = "".join(str.split())

        if ("$" in str):
            self.buy_back_count += 1
        if (str.isdigit()):
            num = int(str)
            # Round down to nearest 100 since you can only have multiples of $100
            # in-game and so anything that's not a multiple of 100 is an OCR error
            return num - (num % 100)
        return 0


import pytesseract
import pyautogui
import cv2

im = pyautogui.screenshot("screenshot.png", region=(0, 0, 100, 200))
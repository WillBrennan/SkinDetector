import cv2
import numpy
import skin_detector


def test_get_hsv_mask():
    img = cv2.imread("../test_image.png")
    mask = skin_detector.get_hsv_mask(img)
    assert img.shape[:2] == mask.shape


def test_get_rgb_mask():
    img = cv2.imread("../test_image.png")
    mask = skin_detector.get_rgb_mask(img)
    assert img.shape[:2] == mask.shape


def test_get_ycrcb_mask():
    img = cv2.imread("../test_image.png")
    mask = skin_detector.get_ycrcb_mask(img)
    assert img.shape[:2] == mask.shape


def test_grab_cut_mask():
    img = cv2.imread("../test_image.png")
    assert True


def test_closing():
    img = cv2.imread("../test_image.png")
    assert True


def test_process():
    img = cv2.imread("../test_image.png")
    assert True

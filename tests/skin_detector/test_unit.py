import cv2
import os
import numpy
import skin_detector


def test_get_hsv_mask():
    img_path = "tests/test_image.png"
    img = cv2.imread(img_path)
    mask = skin_detector.get_hsv_mask(img)
    assert img.shape[:2] == mask.shape


def test_get_rgb_mask():
    img_path = "tests/test_image.png"
    img = cv2.imread(img_path)
    mask = skin_detector.get_rgb_mask(img)
    assert img.shape[:2] == mask.shape


def test_get_ycrcb_mask():
    img_path = "tests/test_image.png"
    img = cv2.imread(img_path)
    mask = skin_detector.get_ycrcb_mask(img)
    assert img.shape[:2] == mask.shape


def test_grab_cut_mask():
    img_path = "tests/test_image.png"
    img = cv2.imread(img_path)
    assert True


def test_closing():
    img_path = "tests/test_image.png"
    img = cv2.imread(img_path)
    assert True


def test_process():
    img_path = "tests/test_image.png"
    img = cv2.imread(img_path)
    mask = skin_detector.process(img)
    assert img.shape[:2] == mask.shape

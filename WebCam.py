#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
import argparse
import logging
# Standard Modules
import cv2
# Custom Modules
import scripts
from SkinDetector import SkinDetector


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image_paths', type=str, nargs='+', help="paths to one or more images or image directories")
    parser.add_argument('-b', '--debug', dest='debug', action='store_true', help='enable debug logging')
    parser.add_argument('-q', '--quite', dest='quite', action='store_true', help='disable all logging')
    parser.add_argument('-t', '--thresh', dest='thresh', default=0.5, type=float, help='threshold for skin mask')
    args = parser.parse_args()

    logger = logging.getLogger('main')
    if not args.quite:
        if args.debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        ch = logging.StreamHandler()
        ch.setLevel(level=level)
        formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    detector = SkinDetector(args)

    cam = cv2.VideoCapture(0)
    while True:
        ret, img_col = cam.read()
        img_msk = detector.process(img_col)
        if not args.display:
            scripts.display('img_col', img_col)
            scripts.display('img_msk', img_msk)
            scripts.display('img_skn', cv2.bitwise_and(img_col, img_col, mask=img_msk))
            cv2.waitKey(5)
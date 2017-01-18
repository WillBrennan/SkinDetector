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
    parser.add_argument('-b', '--debug', dest='debug', action='store_true', help='enable debug logging')
    parser.add_argument('-t', '--thresh', dest='thresh', default=0.5, type=float, help='threshold for skin mask')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")

    detector = SkinDetector(thresh=args.thresh, debug=args.debug)

    cam = cv2.VideoCapture(0)
    logging.info("press any key to exit")

    while True:
        ret, img_col = cam.read()
        img_msk = detector.process(img_col)

        scripts.display('img_col', img_col)
        scripts.display('img_msk', img_msk)
        scripts.display('img_skn', cv2.bitwise_and(img_col, img_col, mask=img_msk))

        waitkey = cv2.waitKey(5)
        if waitkey != -1:
            break

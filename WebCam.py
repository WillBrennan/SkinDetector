#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
import logging
# Standard Modules
import cv2
import numpy
# Custom Modules
import main
import scripts


if __name__ == '__main__':
    args = scripts.get_args(from_file=False)
    logger = scripts.get_logger(quite=args.quite, debug=args.debug)
    cam = cv2.VideoCapture(0)
    while True:
        ret, img_col = cam.read()
        img_msk = main.process(img_col, args=args)
        if not args.display:
            scripts.display('img_col', img_col)
            scripts.display('img_msk', img_msk)
            scripts.display('img_skn', cv2.bitwise_and(img_col, img_col, mask=img_msk))
            cv2.waitKey(5)
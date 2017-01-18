#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
import os
import argparse
import logging
# Standard Modules
import cv2
import numpy
# Custom Modules
import scripts
from SkinDetector import SkinDetector

logger = logging.getLogger('main')


def find_images(path, recursive=False, ignore=True):
    if os.path.exists(path):
        yield path
    elif os.path.isdir(path):
        assert os.path.isdir(path), 'FileIO - get_images: Directory does not exist'
        assert isinstance(recursive, bool), 'FileIO - get_images: recursive must be a boolean variable'
        ext, result = ['png', 'jpg', 'jpeg'], []
        for path_a in os.listdir(path):
            path_a = path + '/' +path_a
            if os.path.isdir(path_a) and recursive:
                for path_b in find_images(path_a):
                    yield path_b
            check_a = path_a.split('.')[-1] in ext
            check_b = ignore or ('-' not in path_a.split('/')[-1])
            if check_a and check_b:
                yield path_a
    else:
        raise ValueError('error! path is not a valid path or directory')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image_paths', type=str, nargs='+', help="paths to one or more images or image directories")
    parser.add_argument('-b', '--debug', dest='debug', action='store_true', help='enable debug logging')
    parser.add_argument('-q', '--quite', dest='quite', action='store_true', help='disable all logging')
    parser.add_argument('-d', '--display', dest='display', action='store_true', help="display result")
    parser.add_argument('-s', '--save', dest='save', action='store_true', help="save result to file")
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

    for image_arg in args.image_paths:
        for image_path in find_images(image_arg):
            logging.info("loading image from {0}".format(image_path))
            img_col = cv2.imread(image_path, 1)

            img_msk = detector.process(img_col)

            if args.display:
                scripts.display('img_col', img_col)
                scripts.display('img_msk', img_msk)
                scripts.display('img_skn', cv2.bitwise_and(img_col, img_col, mask=img_msk))
                cv2.waitKey(0)
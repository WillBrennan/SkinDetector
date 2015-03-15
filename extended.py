#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
import sys
import argparse
import logging
# Standard Modules
# Custom Modules


def get_logger(level=logging.INFO, quite=False, debug=False, to_file=''):
    """
    This function initialises a logger to stdout.

    :return: logger
    """
    assert level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL]
    logger = logging.getLogger('main')
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    if debug:
        level = logging.DEBUG
    logger.setLevel(level=level)
    if not quite:
        if to_file:
            fh = logging.FileHandler(to_file)
            fh.setLevel(level=level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        else:
            ch = logging.StreamHandler()
            ch.setLevel(level=level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
    return logger


def get_args(default=None, args_string=sys.argv):
    """
    This function gets the command line arguments and passes any unknown arguments to ALE.
    :param default: dictionary of default arguments with keys as `dest`
    :return: command line arguments
    """
    if not default:
        default = {}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image_path', type=str, nargs='+', help="Filepath for input images or folder containing images")
    parser.add_argument('-n', '--name', dest='name', default='DEFAULT_NAME', type=str, help='Basename of all export files')
    parser.add_argument('-b', '--debug', dest='debug', action='store_true', help='Lower logging level to debug')
    parser.add_argument('-q', '--quite', dest='quite', action='store_true', help='Disable all logging entirely')
    parser.add_argument('-d', '--display', dest='display', action='store_true', help="Display Game while learning and testing")
    parser.add_argument('-s', '--save', dest='save', action='store_true', help="If parsed saves the input image and mask with random file name, records name to logger")
    return parser.parse_known_args(args_string)


def gen_args():
    return get_args(args_string='USED_GEN_ARGS')
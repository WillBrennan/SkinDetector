#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
import time
import argparse
import logging
# Standard Modules
import cv2
import numpy
# Custom Modules

logger = logging.getLogger('main')


class SkinDetector(object):
    def __init__(self, args):
        assert isinstance(args, argparse.Namespace), 'args must be of type argparse.Namespace'
        self.args = args
        self.mask = None
        logger.debug('SkinDetector initialised')

    @staticmethod
    def assert_image(img, grey=False):
        logger.debug('Applying assertions...')
        depth = 3
        if grey:
            depth = 2
        assert isinstance(img, numpy.ndarray), 'image must be a numpy array'
        assert len(img.shape) == depth, 'skin detection can only work on color images'
        assert img.size > 100, 'seriously... you thought this would work?'

    def get_mask_hsv(self, img):
        logger.debug('Applying hsv threshold')
        self.assert_image(img)
        lower_thresh = numpy.array([0, 50, 0], dtype=numpy.uint8)
        upper_thresh = numpy.array([120, 150, 255], dtype=numpy.uint8)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        msk_hsv = cv2.inRange(img_hsv, lower_thresh, upper_thresh)
        if self.args.debug:
            scripts.display('input', img)
            scripts.display('mask_hsv', msk_hsv)
        self.add_mask(msk_hsv)

    def get_mask_rgb(self, img):
        logger.debug('Applying rgb thresholds')
        lower_thresh = numpy.array([45, 52, 108], dtype=numpy.uint8)
        upper_thresh = numpy.array([255, 255, 255], dtype=numpy.uint8)
        mask_a = cv2.inRange(img, lower_thresh, upper_thresh)
        mask_b = 255*((img[:, :, 2]-img[:, :, 1])/20)
        logger.debug('mask_b unique: {0}'.format(numpy.unique(mask_b)))
        mask_c = 255*((numpy.max(img, axis=2)-numpy.min(img, axis=2))/20)
        logger.debug('mask_d unique: {0}'.format(numpy.unique(mask_c)))
        msk_rgb = cv2.bitwise_and(mask_a, mask_b)
        msk_rgb = cv2.bitwise_and(mask_c, msk_rgb)
        if self.args.debug:
            scripts.display('input', img)
            scripts.display('mask_rgb', msk_rgb)
        self.add_mask(msk_rgb)

    def get_mask_ycrcb(self, img):
        self.assert_image(img)
        lower_thresh = numpy.array([90, 100, 130], dtype=numpy.uint8)
        upper_thresh = numpy.array([230, 120, 180], dtype=numpy.uint8)
        img_ycrcb = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)
        msk_ycrcb = cv2.inRange(img_ycrcb, lower_thresh, upper_thresh)
        if self.args.debug:
            scripts.display('input', img)
            scripts.display('mask_ycrcb', msk_ycrcb)
        self.add_mask(msk_ycrcb)

    def grab_cut_mask(self, img_col, mask):
        kernel = numpy.ones((50, 50), numpy.float32)/(50*50)
        dst = cv2.filter2D(mask, -1, kernel)
        dst[dst != 0] = 255
        free = numpy.array(cv2.bitwise_not(dst), dtype=numpy.uint8)
        if self.args.debug:
            scripts.display('not skin', free)
            scripts.display('grabcut input', mask)
        grab_mask = numpy.zeros(mask.shape, dtype=numpy.uint8)
        grab_mask[:, :] = 2
        grab_mask[mask == 255] = 1
        grab_mask[free == 255] = 0
        print numpy.unique(grab_mask)
        if numpy.unique(grab_mask).tolist() == [0, 1]:
            logger.debug('conducting grabcut')
            bgdModel = numpy.zeros((1, 65), numpy.float64)
            fgdModel = numpy.zeros((1, 65), numpy.float64)
            if img_col.size != 0:
                mask, bgdModel, fgdModel = cv2.grabCut(img_col, grab_mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
                mask = numpy.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            else:
                logger.warning('img_col is empty')
        return mask

    @staticmethod
    def closing(msk):
        assert isinstance(msk, numpy.ndarray), 'msk must be a numpy array'
        assert msk.ndim == 2, 'msk must be a greyscale image'
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        msk = cv2.morphologyEx(msk, cv2.MORPH_CLOSE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        msk = cv2.morphologyEx(msk, cv2.MORPH_OPEN, kernel, iterations=2)
        return msk

    def process(self, img):
        logger.debug('Initialising process')
        dt = time.time()
        self.assert_image(img)
        logger.debug('Generating mean-color image')
        #img = mean_color.img_mean(img)
        logger.debug('Conducting thresholding')
        self.n_mask = 0
        self.mask = numpy.zeros(img.shape[:2], dtype=numpy.uint8)
        self.get_mask_hsv(img)
        self.get_mask_rgb(img)
        self.get_mask_ycrcb(img)
        logger.debug('Thresholding sum of masks')
        self.threshold(self.args.thresh)
        if self.args.debug:
            scripts.display('skin_mask', self.mask)
            scripts.display('input_img', img)
        dt = round(time.time()-dt, 2)
        hz = round(1/dt, 2)
        logger.debug('Conducted processing in {0}s ({1}Hz)'.format(dt, hz))
        self.mask = self.closing(self.mask)
        self.mask = self.grab_cut_mask(img, self.mask)
        return self.mask

    def add_mask(self, img):
        logger.debug('normalising mask')
        self.assert_image(img, grey=True)
        img[img < 128] = 0
        img[img >= 128] = 1
        logger.debug('normalisation complete')
        logger.debug('adding mask to total mask')
        self.mask += img
        self.n_mask += 1
        logger.debug('add mask complete')

    def threshold(self, threshold):
        assert isinstance(threshold, float), 'threshold must be a float (current type - {0})'.format(type(threshold))
        assert 0 <= threshold <= 1, 'threshold must be between 0 & 1 (current value - {0})'.format(threshold)
        assert self.n_mask > 0, 'Number of masks must be greater than 0 [n_mask ({0}) = {1}]'.format(type(self.n_mask), self.n_mask)
        logger.debug('Threshold Value - {0}%'.format(int(100*threshold)))
        logger.debug('Number of Masks - {0}'.format(self.n_mask))
        self.mask /= self.n_mask
        self.mask[self.mask < threshold] = 0
        self.mask[self.mask >= threshold] = 255
        logger.debug('{0}% of the image is skin'.format(int((100.0/255.0)*numpy.sum(self.mask)/(self.mask.size))))
        return self.mask
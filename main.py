#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
import time
import argparse
# Standard Modules
import cv2
import numpy
# Custom Modules
import extended


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
        lower_thresh = numpy.array([100, 50, 0], dtype=numpy.uint8)
        upper_thresh = numpy.array([120, 150, 255], dtype=numpy.uint8)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        msk_hsv = cv2.inRange(img_hsv, lower_thresh, upper_thresh)
        if self.args.debug:
            cv2.destroyAllWindows()
            cv2.imshow('input', img)
            cv2.imshow('mask', msk_hsv)
            cv2.waitKey(0)
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
            cv2.destroyAllWindows()
            cv2.imshow('input', img)
            cv2.imshow('mask', msk_rgb)
            cv2.waitKey(0)
        self.add_mask(msk_rgb)

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
        self.n_mask = 0
        #image = self.normalise(image)
        self.mask = numpy.zeros(img.shape[:2], dtype=numpy.uint8)
        self.get_mask_hsv(img)
        self.get_mask_rgb(img)
        logger.debug('Thresholding sum of masks')
        self.threshold(self.args.thresh)
        if self.args.debug:
            cv2.destroyAllWindows()
            cv2.imshow('skin_mask', self.mask)
            cv2.imshow('input_img', img)
            cv2.waitKey(0)
        dt = round(time.time()-dt, 2)
        hz = round(1/dt, 2)
        logger.debug('Conducted processing in {0}s ({1}Hz)'.format(dt, hz))
        self.mask = self.closing(self.mask)
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
        threshold *= self.n_mask
        self.mask /= self.n_mask
        self.mask[self.mask < threshold] = 0
        self.mask[self.mask >= threshold] = 255
        logger.debug('{0}% of the image is skin'.format(int((100.0/255.0)*numpy.sum(self.mask)/(self.mask.size))))
        return self.mask

    def normalise(self, img):
        # todo: this currently messes up with color images
        self.assert_image(img)
        if self.args.debug:
            cv2.imshow('input image', img)
        logger.debug('Normalising brightness and contrast')
        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        div = numpy.float32(img)/(cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel1))
        image = numpy.uint8(cv2.normalize(div, div, 0, 255, cv2.NORM_MINMAX))
        if self.args.debug:
            cv2.imshow('normalised brightness', image)
        logger.debug('Applying Bilateral Filter')
        if self.args.debug:
            cv2.imshow('reduced noise', image)
        if self.args.debug:
            cv2.waitKey(0)
        return image


def process(image, save=False, display=False, args=None):
    assert isinstance(image, numpy.ndarray)
    if not args:
        args = extended.gen_args()
    else:
        assert isinstance(args, argparse.Namespace), 'args must be an argparse.Namespace'
    args.save = save
    args.display = display
    detector = SkinDetector(args)
    return detector.process(image)


if __name__ == '__main__':
    args = extended.get_args()
    logger = extended.get_logger(quite=args.quite, debug=args.debug)
    args.image_paths = extended.find_images(args.image_paths[0])
    for image_path in args.image_paths:
        img_col = cv2.imread(image_path, 1)
        img_msk = process(img_col, args=args)
        if not args.display:
            cv2.destroyAllWindows()
            cv2.imshow('img_col', img_col)
            cv2.imshow('img_msk', img_msk)
            cv2.imshow('img_skn', cv2.bitwise_and(img_col, img_col, mask=img_msk))
            cv2.waitKey(0)
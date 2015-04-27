#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
import logging
# Standard Modules
import cv2
import numpy
# Custom Modules
import mean_color


logger = logging.getLogger('main')


class SuperContour(object):
    def __init__(self, width=32):
        self.width = width

    def grid_contours(self, frame, contours, heir):
        result_cont, result_heir, result_rois = [], [], []
        logger.debug('segmenting contours with grid')
        for contour in contours:
            msk = numpy.zeros(frame.shape, dtype=frame.dtype)
            cv2.drawContours(msk, [contour], -1, 255, -1)
            bbox = cv2.boundingRect(contour)
            w0, h0 = bbox[0]//self.width, bbox[1]//self.width
            n_w = max(1, ((bbox[0]+bbox[2])//self.width) - w0)
            n_h = max(1, ((bbox[1]+bbox[3])//self.width) - h0)
            for i in range(n_w):
                for j in range(n_h):
                    grid_msk = numpy.zeros(frame.shape, dtype=frame.dtype)
                    grid_box = numpy.array([[], [], [], []], dtype=numpy.uint8)
                    cv2.drawContours(grid_msk, [grid_box], -1, 255, -1)
                    grid_msk = cv2.bitwise_and(grid_msk, msk)
                    result_cont.append(grid_msk)
                    # todo: work out stats of new contour!
        # todo: mix grid with contours to form super pixels!
        contours = result_cont
        logger.debug('checking and removing overlap...')
        msk_all = numpy.zeros(frame.shape[:2], dtype=frame.dtype)
        for msk in contours:
            msk = cv2.bitwise_and(msk, cv2.bitwise_not(msk_all))
            if msk.sum() != 0:
                result_cont.append(msk)
                msk_all = numpy.min(255, cv2.add(msk_all, msk))
        logger.debug('grid contours complete')
        contours = result_cont
        return contours, heir, rois

    def process(self, frame):
        frame_gry = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        contours, heir = cv2.findContours(frame_gry, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, heir, rois = self.grid_contours(frame, contours, heir)
        for i in range(len(contours)):
            roi, contour = rois[i], contours[i]
            mask = numpy.zeros(frame.shape[:2], dtype=frame.dtype)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            yield roi, contour
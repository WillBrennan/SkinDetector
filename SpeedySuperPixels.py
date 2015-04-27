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

    def grid_contours(self, contours, heir):
        result_cont, result_heir, result_rois = [], [], []
        # todo: mix grid with contours to form super pixels!
        # todo: remove any regions of overlap!
        result_heir = heir
        return result_cont, result_heir, result_rois

    def process(self, frame):
        frame_gry = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        contours, heir = cv2.findContours(frame_gry, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, heir, rois = self.grid_contours(contours, heir)
        for i in range(len(contours)):
            roi, contour = rois[i], contours[i]
            mask = numpy.zeros(frame.shape, dtype=frame.dtype)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            yield roi, contour
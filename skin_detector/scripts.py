#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'

# Built-in Modules
# Standard Modules
import cv2
import numpy

# Custom Modules


def display(title, img, max_size=200000):
    assert isinstance(img, numpy.ndarray), 'img must be a numpy array'
    assert isinstance(title, str), 'title must be a string'
    scale = numpy.sqrt(min(1.0, float(max_size) / (img.shape[0] * img.shape[1])))
    shape = (int(scale * img.shape[1]), int(scale * img.shape[0]))
    img = cv2.resize(img, shape)
    cv2.imshow(title, img)

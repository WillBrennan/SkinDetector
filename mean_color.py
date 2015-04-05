#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in modules
import time
import logging
# Standard modules
import numpy
import sklearn.utils
import sklearn.cluster as cluster
# Custom modules

logger = logging.getLogger('main')


def img_mean(frame, n_clusters=64):
    result = frame.copy()
    flat_frame = frame.reshape(-1, 3)
    frame = sklearn.utils.shuffle(flat_frame)[:min(1000, frame.shape[0]*frame.shape[1])]
    logger.debug('frame shape: {0}'.format(frame.shape))
    logger.debug('starting training...')
    t0 = time.time()
    kmeans = cluster.KMeans(n_clusters=n_clusters, random_state=0).fit(frame)
    logger.debug('training took {0}s'.format(round(time.time()-t0, 2)))
    lookup = kmeans.predict(flat_frame)
    label_idx = 0
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i][j] = kmeans.cluster_centers_[lookup[label_idx]]
            label_idx += 1
    logger.debug('label shape: {0}'.format(result.shape))
    result.astype(dtype=numpy.uint8)
    return result
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quick utility to make a list of everything cool that happened on the night sky in the last week.

.. currentmodule:: fpi2nite
.. moduleauthor:: hank corbett <htc@unc.edu>
"""
import logging

from .version import __version__, __release__  # noqa


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        logger.setLevel(('INFO'))
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            '%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')
        console.setFormatter(formatter)
    return logger


# For testing
base_log = get_logger(__name__).addHandler(logging.StreamHandler())

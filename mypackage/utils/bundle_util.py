#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import logging

from mypackage.utils.bundle_files import BundleLogs, BundleTarFiles


TUTORIALS_ORDER = [
    'Power_Measurement_Tutorial',
    'Introduction',
    'Parsing',
    'Model_Optimization',
    'Layer_Noise_Analysis',
    'Compilation',
    'Inference',
    'Power_Measurement',
    'Multiple_Models_Tutorial'
    ]


class BundleTestUtil:
    @staticmethod
    def get_tutorials(notebook_path):
        notebook_files = glob.glob(f'{notebook_path}/*.ipynb')
        sorted_files = []
        for task in TUTORIALS_ORDER:
            for notebook in notebook_files:
                if task in notebook:
                    sorted_files.append(notebook)
        return sorted_files


class BundleTestUtilException(Exception):
    pass
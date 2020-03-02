#!/usr/bin python3
# -*- coding: utf-8 -*-

from picamera import PiCamera
from config import configs
import os
"""set camera"""
camera = PiCamera()
camera.resolution = (1000, 1000)
camera.framerate = 60
# 打开预览
i = 0
camera.start_preview()


def take_picture():
    name = configs['picture']['picture_name_fn']()
    camera.capture(os.path.join(configs['picture']['picture_address'], name+'.png'))
    return os.path.join(configs['picture']['picture_address'], name+'.png')




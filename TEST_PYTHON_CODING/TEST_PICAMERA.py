from picamera import PiCamera 
import time 
"""set camera""" 
camera = PiCamera() 
camera.resolution = (1920,1080) 
camera.framerate = 60 
# 打开预览 
camera.start_preview()
time.sleep(5)
camera.capture('/home/pi/testme.jpg') 
camera.stop_preview() 

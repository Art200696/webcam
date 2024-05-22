"""
_webcam_background.py: Contains the _WebcamBackground class, which is a wrapper for the imutils
WebcamVideoStream class. It is used by the Webcam class in webcam.py to read frames from a webcam
running in a background thread. This wrapper tries to make the interface more similar to the
cv2.VideoCapture class, so it can be used as a drop-in replacement for the cv2.VideoCapture class.

Author: Eric Canas
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 05-05-2023
"""
from __future__ import annotations
from imutils.video import WebcamVideoStream
import warnings
import time
import numpy as np

class _WebcamBackground(WebcamVideoStream):
    def __init__(self, src=0, name="WebcamVideoStream", queue_max_length=10):
        super().__init__(src=src, name=name)

        if queue_max_length > 0:
            self.queue_max_length = queue_max_length
            self.frames_queue = []


        # time.sleep(0.25)  # Added delay

    def update(self):
        while True:
            if self.stopped:
                return
            if self.stream.isOpened():  # Check if the stream is opened
                try:
                    (self.grabbed, self.frame) = self.stream.read()
                except:
                    self.grabbed = False
                    self.frame = np.ones_like((10, 10))
                if self.queue_max_length > 0:
                    if len(self.frames_queue) >= self.queue_max_length:
                        self.frames_queue = self.frames_queue[:-1]
                    self.frames_queue.append(self.frame)
                    

    def read_batch(self, batch_size=10):
        if batch_size > self.queue_max_length:
            warnings.warn(f"Batch size error: {batch_size=} while {self.queue_max_length=}. Setting batch size to Queue Max Length.")
            batch_size = self.queue_max_length
        return_batch = self.frames_queue[-batch_size:]
        self.frames_queue = self.frames_queue[:-batch_size]
        return [1]*len(return_batch), return_batch
    
    def read(self):
        frame = super().read()
        return self.grabbed, frame

    def stop(self):
        super().stop()
        self.grabbed = False

    def get(self, propId):
        return self.stream.get(propId=propId)

    def set(self, propId, value):
        self.stream.set(propId=propId, value=value)

    def release(self):
        self.stream.release()

    def isOpened(self):
        return self.stream.isOpened()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.release()

    def __del__(self):
        self.stop()
        self.release()

    def __iter__(self):
        return self

    def __next__(self):
        return self.read()

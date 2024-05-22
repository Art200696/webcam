from __future__ import annotations
import cv2
from webcam import Webcam
import os
import numpy as np
from matplotlib import pyplot as plt

FRAMES_TO_READ = 50000



if __name__ == '__main__':

    # Instantiate a Webcam instance with the background parameter
    webcam = Webcam(#src=1,
                    src=0,
                    w=640, run_in_background=True,
                    on_aspect_ratio_lost='resize')

    # Iteratively read FRAMES_TO_READ frames
    for ret, frame in webcam.read_batch():
        
        cv2.imshow('Webcam Frame', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the resources and close the window
    webcam.release()
    cv2.destroyAllWindows()
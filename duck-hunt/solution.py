import time
import cv2
import numpy as np
import os

"""
Replace following with your own algorithm logic

Two random coordinate generator has been provided for testing purposes.
Manual mode where you can use your mouse as also been added for testing purposes.
"""
def GetLocation(move_type, env, current_frame):
    #time.sleep(1) #artificial one second processing time
    
    #Use relative coordinates to the current position of the "gun", defined as an integer below
    if move_type == "relative":
        """
        North = 0
        North-East = 1
        East = 2
        South-East = 3
        South = 4
        South-West = 5
        West = 6
        North-West = 7
        NOOP = 8
        """
        coordinate = env.action_space.sample() 
    #Use absolute coordinates for the position of the "gun", coordinate space are defined below
    else:
        """
        (x,y) coordinates
        Upper left = (0,0)
        Bottom right = (W, H) 
        """

        #coordinate = env.action_space_abs.sample()
        coordinate = (0,0)
        ## Check if last frame exists
        if (os.path.exists("last_frame.png")):

            last_frame = cv2.imread("last_frame.png", 0)
            current_frame = cv2.resize(cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY), None, fx=0.5, fy=0.5)

            ## Calculate difference
            frame_difference = np.abs(current_frame - last_frame)
            coordinate = findDuck(frame_difference)
            cv2.imwrite("last_frame.png", current_frame)
            return [{'coordinate' : coordinate, 'move_type' : move_type}]
            
        else:
            cv2.imwrite("last_frame.png", cv2.resize(cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY), None, fx=0.5, fy=0.5))
            coordinate = env.action_space.sample()
    
    return [{'coordinate' : coordinate, 'move_type' : move_type}]

## Function for searching for ducks using Blob Detection
def findDuck(image):

    ## Set searching params
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByCircularity = True
    params.maxCircularity = 0.9
    params.minArea = 5

    ## Create Detector
    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(image)

    if (len(keypoints) > 0):
        ## Due to dead ducks being targetted, add randomness to next target
        ## TODO: Find a way to not include dead ducks (Look into tracking velocity of objects)
        x, y = keypoints[np.random.randint(0, len(keypoints))].pt
    else:
        (x, y) = (0, 0)

    return (y*2,x*2)




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
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY)

            ## Calculate difference
            frame_difference = cv2.subtract(current_frame, last_frame)
            cv2.imwrite("output.png", frame_difference)
            #print(frame_difference)

            ## Blob detection on difference
            x, y = frame_difference.shape[::-1]

            blob_counter = 0
            blob_threshold = 6

            for coord_x in range(0,x-1,3):
                for coord_y in range(0,y-1,3):
                    if (frame_difference[coord_y][coord_x] > 1):
                        blob_counter += 1
                    else:
                        blob_counter = 0

                    if (blob_counter >= blob_threshold):
                        #print(f"Duck found at: {coord_x}, {coord_y}")
                        coordinate = (coord_y, coord_x)
                        cv2.imwrite("last_frame.png", cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR))
                        return [{'coordinate' : coordinate, 'move_type' : move_type}]



            #print(keypoints)

        else:
            cv2.imwrite("last_frame.png", cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR))
            coordinate = (0,0)
        ##duck_image = cv2.imread("duck-images/duck10.png", 0)

        ## Call find duck to get coords
        ##coordinate = findDuck(current_frame, duck_image, 0.8)
    
    return [{'coordinate' : coordinate, 'move_type' : move_type}]

## Function for searching for ducks using template matching
def findDuck(game_screen, duck_image, threshold):

    ## Get grayscale of game frame
    grey_game_screen = cv2.cvtColor(game_screen, cv2.COLOR_BGR2GRAY)

    ## Get grayscale of duck_image
    #grey_duck = cv2.cvtColor(duck_image, cv2.COLOR_BGR2GRAY)

    ## Get dimensions of duck
    w, h = duck_image.shape[::-1]

    ## Call match template to find a duck
    res = cv2.matchTemplate(grey_game_screen, duck_image, cv2.TM_CCOEFF_NORMED)
    
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        #cv2.rectangle(game_screen, pt, (pt[0]+w, pt[1]+h), (0,0,255), 2)
        print("Duck Found!")
        return pt[0], pt[1]
    ## return coordinates of first found duck
    print("NO DUCKS HERE!")
    return 0,0


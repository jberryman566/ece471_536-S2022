import time
import cv2

"""
Replace following with your own algorithm logic

Two random coordinate generator has been provided for testing purposes.
Manual mode where you can use your mouse as also been added for testing purposes.
"""
def GetLocation(move_type, env, current_frame):
    time.sleep(1) #artificial one second processing time
    
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
        coordinate = env.action_space_abs.sample()

        duck_image = cv2.imread("duck_images/green_duck.png")

        ## Call find duck to get coords
        coordinate = findDuck(current_frame, duck_image, 0.8)
    
    return [{'coordinate' : coordinate, 'move_type' : move_type}]

## Function for searching for ducks using template matching
def findDuck(game_screen, duck_image, threshold):

    ## Get grayscale of game frame
    grey_game_screen = cv2.cvtColor(game_screen, cv2.COLOR_BGR2GRAY)

    ## Get grayscale of duck_image
    grey_duck = cv2.cvtColor(duck_image, cv2.COLOR_BGR2GRAY)

    ## Get dimensions of duck
    w, h = grey_duck.shape[::-1]

    ## Call match template to find a duck
    res = cv2.matchTemplate(grey_game_screen, grey_duck, cv2.TM_CCOEFF_NORMED)
    
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(game_screen, pt, (pt[0]+w, pt[1]+h), (0,0,255), 2)

    ## return coordinates of first found duck
    return loc[0][0], loc[0][1]


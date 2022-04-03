import cv2
import numpy as np

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


#### MAIN ####

## Grab sample image 
screen = cv2.imread("sample_game_screen.PNG")

## Grab duck
duck_image = cv2.imread("duck_test.PNG", 0)

coords = findDuck(screen, duck_image, 0.7)

print(coords)
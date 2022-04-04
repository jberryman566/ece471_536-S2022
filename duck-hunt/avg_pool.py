import numpy as np

## Function for calculatimng average pool of an image (1 channel).
# Defaults for kernel and stride are 2
def avgPool(image, kernel_size=2, stride=2):
    
    ## Check if kernel is divisible by kernel size in width and height
    height, width = image.shape[::-1]

    new_image = np.zeros(height/2, width/2)
    y_counter = 0
    x_counter = 0

    for y in range(0, height, 2):
        for x in range(0, width, 2):
            avg = (image[y][x] + image[y][x+1] + image[y+1][x] + image[y+1][x+1])/4
            new_image[y_counter][x_counter] = avg
            x_counter += 1

        y_counter += 1

    
    return new_image

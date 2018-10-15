import numpy as np
import cv2


def mirror(original, axis):
    """mirror effect

    Creates a mirrored version of an already finished image.

    Arguments:
        image: The finished image
               finished means it already has the shapes and colors

        axis:
         "h" for horizontal
         "v" for vertical
         "-h" horizontal, mirror the lower part
         "-v" vertical, mirror the right part
         None, if no mirroring should be made

    Returns:
        image: Image,
               can be the exact same, if axis == None,
               or the mirrored version otherwise
    """
    if not axis:
        return original

    image = original.copy()
    height, width, channels = image.shape
    if axis == "h":
        box = (0, 0, int(height/2), width)
        flip_method = 0
        paste_point = (int(height/2), 0, height, width)
    elif axis == "v":
        box = (0, 0, height, int(width/2))
        flip_method = 1
        paste_point = (0, int(width/2), height, width)
    elif axis == "-h":
        box = (int(height/2), 0, height, width)
        flip_method = 0
        paste_point = (0, 0, int(height/2), width)
    elif axis == "-v":
        box = (0, int(width/2), height, width)
        flip_method = 1
        paste_point = (0, 0, height, int(width/2))
    else:
        print("post_effects.mirror error, axis %s not supported" % axis)
        exit(0)

    flipped = cv2.flip(image[box[0]:box[2], box[1]:box[3]], flip_method)
    image[paste_point[0]:paste_point[2], paste_point[1]:paste_point[3]] = flipped
    return image


def mirror_box(original, axis):
    """mirror box effect

    Choose a random box and apply a mirror efect

    Arguments:
        image: The finished image
               finished means it already has the shapes and colors

        axis:
         "h" for horizontal
         "v" for vertical
         None, if no mirroring should be made

    Returns:
        image: Image,
               can be the exact same, if axis == None,
               or the mirrored version otherwise
    """
    if not axis:
        return original

    image = original.copy()
    height, width, channels = image.shape
    x_initial = np.random.randint(0, width)
    y_initial = np.random.randint(0, height)
    x_final = np.random.randint(x_initial, width+1)
    y_final = np.random.randint(y_initial, height+1)

    box = (y_initial, x_initial, y_final, x_final)
    if axis == "h":
        flip_method = 0
    elif axis == "v":
        flip_method = 1
    else:
        print("post_effects.mirror_box error, axis %s not supported" % axis)
        exit(0)

    flipped = cv2.flip(image[box[0]:box[2], box[1]:box[3]], flip_method)
    image[box[0]:box[2], box[1]:box[3]] = flipped
    return image

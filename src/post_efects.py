from PIL import Image


def mirror(image, axis):
    """
    mirror effect

    Creates a mirrored version of an already finished image.

    Arguments:
        image: The finished PIL image
               finished means it already has the shapes and colors

        axis:
         "h" for horizontal
         "v" for vertical
         "-h" horizontal, mirror the lower part
         "-v" vertical, mirror the right part
         None, if no mirroring should be made

    Returns:
        image: A PIL Image,
               can be the exact same, if axis == None,
               or the mirrored version otherwise
    """
    if not axis:
        return image

    width, height = image.size
    if axis == "h":
        box = (0, 0, width, int(height/2))
        flip_method = Image.FLIP_TOP_BOTTOM
        paste_point = (0, int(height/2))
    elif axis == "v":
        box = (0, 0, int(width/2), height)
        flip_method = Image.FLIP_LEFT_RIGHT
        paste_point = (int(width/2), 0)
    elif axis == "-h":
        box = (0, int(height/2), width, height)
        flip_method = Image.FLIP_TOP_BOTTOM
        paste_point = (0, 0)
    elif axis == "-v":
        box = (int(width/2), 0, width, height)
        flip_method = Image.FLIP_LEFT_RIGHT
        paste_point = (0, 0)
    else:
        print("post_effects error, axis %s not supported" % axis)
        exit(0)

    flipped = image.crop(box).transpose(flip_method)
    image.paste(flipped, paste_point)

    return image

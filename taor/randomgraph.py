"""
randomgraph module.
Uses shape_factory to create a new random image
"""
import numpy as np
from numpy.random import choice
from taor.shape_factory import ShapeFactory
from taor.post_efects import mirror, mirror_box
import cv2

config = dict(
    # use alpha [False, True]
    p_use_alpha=[0.7, 0.3],

    s_quantity=[1, 2, 3, 4],
    p_quantity=[0.55, 0.30, 0.10, 0.05],

    # size of the canvas and the probability of each one
    s_size=[512, 1024, 2048],
    p_size=[0.3, 0.6, 0.1],

    s_aspect=["1:1", "4:3", "16:9"],
    p_aspect=[0.3, 0.5, 0.2],

    # mirror a box
    s_mirror_box=[None, "h", "v"],
    p_mirror_box=[0.95, 0.025, 0.025],

    # mirroring in half, negative means lowerX or rightY
    s_mirroring=[None, "h", "v", "-h", "-v"],
    p_mirroring1=[0.90, 0.025, 0.025, 0.025, 0.025],
    p_mirroring2=[0.90, 0.025, 0.025, 0.025, 0.025]
)


def random_image(file_name=None, dont_show=True, debug=False, seed=None):
    """
    image

    Create a new random image and save it to file_name
    """
    if seed:
        np.random.seed(seed)

    # v1.2
    use_alpha = choice([False, True], p=config["p_use_alpha"])
    quantity = choice(config["s_quantity"], p=config["p_quantity"])
    size = choice(config["s_size"], p=config["p_size"])

    # v1.2
    aspect = choice(config["s_aspect"], p=config["p_aspect"])
    aspect = int(aspect.split(":")[0]), int(aspect.split(":")[1])
    mirroring_axis1 = choice(config["s_mirroring"], p=config["p_mirroring1"])
    mirroring_axis2 = choice(config["s_mirroring"], p=config["p_mirroring2"])
    mirror_box_axis = choice(config["s_mirror_box"], p=config["p_mirror_box"])

    if debug:
        print("Selected values: ")
        print("use alpha = %s" % use_alpha)
        print("quantity of shapes = %d" % quantity)
        print("size = %d" % size)
        print("aspect ratio = %d:%d" % (aspect[0], aspect[1]))
        print("mirroring box axis = %r" % mirror_box_axis)
        print("mirroring axis 1 = %r" % mirroring_axis1)
        print("mirroring axis 2 = %r" % mirroring_axis2)

    factory = ShapeFactory(size)

    canvas = np.zeros((int((size/aspect[0])*aspect[1]), size, 3), np.uint8)
    canvas[:] = factory.get_rgb_color(use_alpha)[:3]
    img = canvas.copy()

    # avoid empty canvas
    while np.count_nonzero(cv2.absdiff(canvas, img)) == 0:
        for _ in range(quantity):
            factory.create_shape(use_alpha).draw(img)
        # post effects
        img = mirror_box(img, mirror_box_axis)
        img = mirror(img, mirroring_axis1)
        img = mirror(img, mirroring_axis2)

    if file_name:
        if ".png" not in file_name.lower():
            file_name += ".png"
        cv2.imwrite(file_name, img)

    if not dont_show:
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

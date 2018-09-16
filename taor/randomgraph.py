"""
randomgraph module.
Uses shape_factory to create a new random image
"""
import numpy as np
from PIL import Image, ImageDraw, ImageChops
from numpy.random import choice
from taor.shape_factory import ShapeFactory
from taor.post_efects import mirror, mirror_box


def random_image(file_name=None, show=False, debug=False, seed=None):
    """
    image

    Create a new random image and save it to file_name
    """
    if seed:
        np.random.seed(seed)

    config = dict(
        # color, grayscale or black and white and their probabilities
        # for now V2 is only color
        s_colorset=["color", "gs", "bw"],
        p_colorset=[1, 0, 0],

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

    # chose colorset, quantity of shapes and size from config
    colorset = choice(config["s_colorset"], p=config["p_colorset"])
    # v1.2
    use_alpha = choice([False, True], p=config["p_use_alpha"])
    colorset_info = {"colorset": colorset, "use_alpha": use_alpha}
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
        print("colorset = %s" % colorset_info['colorset'])
        print("use alpha = %s" % colorset_info['use_alpha'])
        print("quantity of shapes = %d" % quantity)
        print("size = %d" % size)
        print("aspect ratio = %d:%d" % (aspect[0], aspect[1]))
        print("mirroring box axis = %r" % mirror_box_axis)
        print("mirroring axis 1 = %r" % mirroring_axis1)
        print("mirroring axis 2 = %r" % mirroring_axis2)

    factory = ShapeFactory(size)
    canvas = Image.new(
        'RGB',
        (size, int((size/aspect[0])*aspect[1])),
        color=factory.get_color_from_set(colorset_info)
    )
    img = canvas.copy()

    # avoid empty canvas
    while ImageChops.difference(canvas, img).getbbox() is None:
        draw = ImageDraw.Draw(img, 'RGBA')
        for _ in range(quantity):
            factory.create_shape(colorset_info).draw(draw)
        # post effects
        img = mirror_box(img, mirror_box_axis)
        img = mirror(img, mirroring_axis1)
        img = mirror(img, mirroring_axis2)

    if file_name:
        if ".png" not in file_name.lower():
            file_name += ".png"
        img.save(file_name, "PNG")

    if show:
        img.show()

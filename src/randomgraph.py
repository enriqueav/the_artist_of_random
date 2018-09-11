"""
randomgraph module.
Uses shape_factory to create a new random image
"""
from PIL import Image, ImageDraw
from numpy.random import choice
from shape_factory import ShapeFactory
from post_efects import mirror


def image(file_name=None, show=False, debug=False):
    """
    image

    Create a new random image and save it to file_name
    """
    config = dict(
        # color, grayscale or black and white and their probabilities
        s_colorset=["color", "gs", "bw"],
        p_colorset=[0.4, 0.3, 0.3],

        # use alpha [False, True]
        p_use_alpha=[0.7, 0.3],

        # quantity of shapes to add and their probabilities
        s_quantity=[
            1, 2, 3, 4, 5, 6,
            7, 8, 9, 10, 50, 100],
        p_quantity=[
            0.05, 0.19, 0.21, 0.15, 0.11, 0.10,
            0.06, 0.05, 0.05, 0.01, 0.01, 0.01],
        # size of the canvas and the probability of each one
        s_size=[128, 256, 512, 1024, 2048],
        p_size=[0.1, 0.1, 0.3, 0.4, 0.1],

        s_aspect=["1:1", "4:3", "16:9"],
        p_aspect=[0.3, 0.5, 0.2],

        # mirroring in half, negative means lowerX or rightY
        s_mirroring=[None, "h", "v", "-h", "-v"],
        p_mirroring1=[0.90, 0.025, 0.025, 0.025, 0.025],
        p_mirroring2=[0.92, 0.02, 0.02, 0.02, 0.02]
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

    if debug:
        print("Selected values: ")
        print("colorset = %s" % colorset_info['colorset'])
        print("use alpha = %s" % colorset_info['use_alpha'])
        print("quantity of shapes = %d" % quantity)
        print("size = %d" % size)
        print("aspect ratio = %d:%d" % (aspect[0], aspect[1]))
        print("mirroring axis 1 = %r" % mirroring_axis1)
        print("mirroring axis 2 = %r" % mirroring_axis2)

    factory = ShapeFactory(size)
    img = Image.new(
        'RGB',
        (size, int((size/aspect[0])*aspect[1])),
        color=factory.get_color_from_set(colorset_info)
    )
    draw = ImageDraw.Draw(img, 'RGBA')

    for _ in range(quantity):
        factory.create_shape(colorset_info).draw(draw)

    img = mirror(img, mirroring_axis1)
    img = mirror(img, mirroring_axis2)

    if file_name:
        img.save(file_name)

    if show:
        img.show()

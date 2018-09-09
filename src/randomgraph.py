"""
randomgraph module.
Uses shape_factory to create a new random image
"""
from PIL import Image, ImageDraw
from numpy.random import choice
from shape_factory import ShapeFactory


def image(file_name, debug=False):
    """
    image

    Create a new random image and save it to file_name
    """
    config = dict(
        # color, grayscale or black and white and their probabilities
        s_colorset=["color", "gs", "bw"],
        p_colorset=[0.4, 0.3, 0.3],
        # quantity of shapes to add and their probabilities
        s_quantity=[
            1, 2, 3, 4, 5, 6,
            7, 8, 9, 10, 50, 100],
        p_quantity=[
            0.13, 0.17, 0.18, 0.12, 0.11, 0.10,
            0.06, 0.05, 0.05, 0.01, 0.01, 0.01],
        # size of the canvas and the probability of each one
        s_size=[128, 256, 512, 1024, 2048],
        p_size=[0.0, 0.0, 0.0, 0.0, 1]
    )
    # chose colorset, quantity of shapes and size from config
    color_set = choice(config["s_colorset"], p=config["p_colorset"])
    quantity = choice(config["s_quantity"], p=config["p_quantity"])
    size = choice(config["s_size"], p=config["p_size"])

    if debug:
        print("Selected values: ")
        print("colorset = "+color_set)
        print("quantity of shapes="+str(quantity))
        print("size = "+str(size))

    factory = ShapeFactory(size)
    img = Image.new(
        'RGB',
        (size, size),
        color=factory.get_color_from_set(color_set)
    )
    draw = ImageDraw.Draw(img)

    for _ in range(0, quantity):
        factory.create_shape(color_set).draw(draw)

    img.save(file_name)

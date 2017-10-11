"""
randomgraph module.
Uses ShapeFactory to create a new random image
"""
from PIL import Image, ImageDraw
from numpy.random import choice
from shape_factory import ShapeFactory

def image(file_name):
    """
    image

    Create a new random image and save it to file_name
    """
    config = dict(
        s_colorset=["color", "gs", "bw"], #color, grayscale or blackandwhite
        p_colorset_color=0.6,
        p_colorset_gs=0.2,
        p_colorset_bw=0.2,
        s_quantity=[
            1, 2, 3, 4, 5, 6,
            7, 8, 9, 10, 50, 100],
        p_quantity=[
            0.13, 0.17, 0.18, 0.12, 0.11, 0.10,
            0.06, 0.05, 0.05, 0.01, 0.01, 0.01],
        s_size=[100, 200, 400, 800],
        p_size=[0.1, 0.2, 0.6, 0.1]
    )
    p_colorset = [
        config["p_colorset_color"],
        config["p_colorset_gs"],
        config["p_colorset_bw"]]
    size = choice(config["s_size"], p=config["p_size"])
    factory = ShapeFactory(size)

    color_set = choice(config["s_colorset"], p=p_colorset)
    img = Image.new(
        'RGB',
        (size, size),
        color=factory.get_color_from_set(color_set))

    draw = ImageDraw.Draw(img)

    #print("size = "+str(size))
    #print("colorset = "+colorSet)
    #print("quantity of shapes="+str(quantity))

    quantity = choice(config["s_quantity"], p=config["p_quantity"])
    for _ in range(0, quantity):
        factory.create_shape(color_set).draw(draw)

    img.save(file_name)

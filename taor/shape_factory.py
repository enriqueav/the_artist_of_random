"""
shapeFactory module.
Contains the abstract class Shape and all its children
"""
from numpy.random import choice, randint
from taor.shapes import SimpleShape, Rectangle, Circle, Ellipse, Polygon
from taor.generators import Lasso, Explosion, StainGrid, Worm


class ShapeFactory(object):
    """
    shapefactory class.
    The factory class needs to be instantiated, it does not have the factory
    method as Abstract
    """
    def __init__(self, size):
        self.size = size
        self.config = dict(
            s_polygon_points=[6, 8, 10, 12, 14, 16],
            p_polygon_points=[0.3, 0.28, 0.17, 0.12, 0.08, 0.05],

            s_shapes=["r", "c", "e", "p", "l", "x", "s", "w"],
            # p_shapes=[0.05, 0.1, 0.05, 0.1, 0.15, 0.20, 0.18, 0.15],
            p_shapes=[0.05, 0.06, 0.05, 0.12, 0.21, 0.14, 0.20, 0.17],

            # repetition False, True
            p_repetition=[0.1, 0.9],
            s_offset_direction=["x", "y", "xy"],
            p_offset_direction=[0.4, 0.4, 0.2],

            p_outline_color=[0.9, 0.1],
            # Going to be unsupported
            # p_outline_gs=[0.7, 0, 0.15, 0.15],
            # p_outline_bw=[0.8, 0, 0, 0.2]
        )

    @classmethod
    def get_rgb_color(cls, use_alpha=False):
        """
        get_color

        Get 4 values representing R, G, B and Alpha picked at random
        """
        alpha = 255
        red = randint(0, 256)
        green = randint(0, 256)
        blue = randint(0, 256)
        if use_alpha:
            alpha = randint(0, 256)
        return red, green, blue, alpha

    def get_color_from_set(self, color_info):
        """
        get_color_from_set

        Depending on the colorset ("color", "bw", "gs") return a color
        at random
        """
        colorset = color_info["colorset"]
        use_alpha = color_info["use_alpha"]

        if colorset == "color":
            color = self.get_rgb_color(use_alpha=use_alpha)
        else:
            raise ValueError("Unsupported color set BW and GS are going to disappear")
        return color

    def get_random_value(self):
        """
        get_random_value

        Return a random value between 0 and the size of the canvas +- size/6
        """
        delta = int(self.size/6)
        return randint(-delta, self.size+delta)

    def get_coordinates(self, quantity):
        """
        get_coordinates

        Get a list of random values with. The size of the list will be quantity
        """
        return [self.get_random_value() for _ in range(quantity)]

    def get_outline_color_from_set(self, colorset_info):
        """
        get_outline_color_from_set

        Get the color of the outline, depending on the colorset chosen
        ("color", "gs" or "bw") the logic if different
        """
        colorset = colorset_info["colorset"]
        # This needs to be executed every time to get new random values
        colors = [None, self.get_rgb_color()]
        if colorset == "color":
            color = choice(colors, p=self.config["p_outline_color"])
        else:
            raise ValueError("Unsupported color set BW and GS are going to disappear")
        return color

    def create_shape(self, colorset_info):
        """
        create_shape

        This is the factory method. Pick a Shape type at random, taking
        from self.config["s_shapes"], with the probabilities
        given by self.config["p_shapes"].

        Additionally, it may add a repetition offset to the shape created
        """
        shape_type = choice(self.config["s_shapes"], p=self.config["p_shapes"])
        color = self.get_color_from_set(colorset_info)
        outline = self.get_outline_color_from_set(colorset_info)

        if shape_type == "r":
            shape = Rectangle(self.get_coordinates(4), color, outline)
        elif shape_type == "e":
            shape = Ellipse(self.get_coordinates(4), color, outline)
        elif shape_type == "c":
            shape = Circle(self.get_coordinates(3), color, outline)
        elif shape_type == "p":
            how_many_vertices = choice(
                self.config["s_polygon_points"],
                p=self.config["p_polygon_points"]
            )
            shape = Polygon(self.get_coordinates(how_many_vertices), color, outline)
        elif shape_type == "l":
            shape = Lasso(self.get_coordinates(2), color)
        elif shape_type == "x":
            shape = Explosion(self.get_coordinates(2), color)
        elif shape_type == "s":
            shape = StainGrid(self.get_coordinates(2), color)
        elif shape_type == "w":
            shape = Worm(self.get_coordinates(2), color)
        else:
            print("shape_factory.create_shape error, shape %s not supported" % shape_type)
            exit(0)

        repetition = choice(a=[True, False], p=self.config["p_repetition"])
        if isinstance(shape, SimpleShape) and repetition:
            offset_direction = choice(
                self.config["s_offset_direction"],
                p=self.config["p_offset_direction"]
            )
            x_offset = 0
            y_offset = 0
            limit = self.size/2
            if offset_direction.find("x") >= 0:
                x_offset = randint(-limit, limit)
            if offset_direction.find("y") >= 0:
                y_offset = randint(-limit, limit)
            repetitions = randint(2, 10)
            shape.set_repetition(x_offset, y_offset, repetitions)

        return shape

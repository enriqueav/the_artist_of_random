"""
shapeFactory module.
Contains the abstract class Shape and all its children
"""
from numpy.random import choice, randint
from shapes import Rectangle, Ellipse, Circle, Polygon


class ShapeFactory(object):
    """
    shapefactory class.
    The factory class needs to be instantiated, it does not have the factory
    method as Abstract
    """
    s_shapes = ["r", "c", "e", "p"]

    def __init__(self, size):
        self.size = size
        self.config = dict(
            s_polygon_points=[6, 8, 10, 12, 14, 16],
            p_polygon_points=[0.3, 0.28, 0.17, 0.12, 0.08, 0.05],

            s_shapes=["r", "c", "e", "p"],
            p_shapes=[0.4, 0.3, 0.2, 0.1],

            p_repetition=[0.1, 0.9],
            s_offset_direction=["x", "y", "xy"],
            p_offset_direction=[0.4, 0.4, 0.2],

            p_outline_color=[0.7, 0.1, 0.1, 0.1],
            p_outline_gs=[0.7, 0, 0.15, 0.15],
            p_outline_bw=[0.8, 0, 0, 0.2]
        )

    @classmethod
    def get_rgb_color(cls):
        """
        get_color

        Get a tuple of 3 values representing R, G, B picked at random
        """
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        return red, green, blue

    @classmethod
    def get_bw(cls):
        """
        get_bw

        Return "white" or "black" with equal probability
        """
        return choice(["white", "black"])

    @classmethod
    def get_gray(cls):
        """
        get_gray

        Return an RGB color where r == g == b, meaning, is a gray
        """
        level = randint(0, 255)
        return level, level, level

    def get_color_from_set(self, colorset):
        """
        get_color_from_set

        Depending on the colorset ("color", "bw", "gs") return a color
        at random
        """
        if colorset == "color":
            color = self.get_rgb_color()
        elif colorset == "bw":
            color = self.get_bw()
        elif colorset == "gs":
            color = self.get_gray()
        else:
            raise ValueError("Unsupported color set ")
        return color

    def get_random_value(self):
        """
        get_random_value

        Return a random value between 0 and the size of the canvas
        """
        return randint(0, self.size)

    def get_coordinates(self, quantity):
        """
        get_coordinates

        Get a list of random values with. The size of the list will be quantity
        """
        return [self.get_random_value() for _ in range(0, quantity)]

    def get_outline_color_from_set(self, colorset):
        """
        get_outline_color_from_set

        Get the color of the outline, depending on the colorset chosen
        ("color", "gs" or "bw") the logic if different
        """
        # This needs to be executed every time to get new random values
        colors = [None, self.get_rgb_color(), self.get_gray(), self.get_bw()]
        if colorset == "color":
            color = choice(colors, p=self.config["p_outline_color"])
        elif colorset == "gs":
            color = choice(colors, p=self.config["p_outline_gs"])
        elif colorset == "bw":
            color = choice(colors, p=self.config["p_outline_bw"])
        else:
            raise ValueError("Unsupported color set ")
        return color

    def create_shape(self, colorset="color"):
        """
        create_shape

        This is the factory method. Pick a Shape type at random, taking
        from self.config["s_shapes"], with the probabilities
        given by self.config["p_shapes"].

        Additionally, it may add a repetition offset to the shape created
        """
        shape_type = choice(self.config["s_shapes"], p=self.config["p_shapes"])
        color = self.get_color_from_set(colorset)
        outline = self.get_outline_color_from_set(colorset)

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

        if choice(a=[True, False], p=self.config["p_repetition"]):
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

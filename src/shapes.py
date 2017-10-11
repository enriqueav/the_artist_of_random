"""
Shapes module.
Contains the abstract class Shape and all its children
"""
from abc import ABCMeta, abstractmethod


class Shape(object):
    """
    Shapes class.
    Abstract class to represent a Shape to be drawn in a PIL image
    """
    __metaclass__ = ABCMeta

    def __init__(self, coordinates, color, outline):
        self.coordinates = coordinates
        self.color = color
        self.outline = outline
        self.x_offset = 0
        self.y_offset = 0
        self.repetitions = 1

    def set_repetition(self, x_offset, y_offset, repetitions):
        """
        set_repetition

        Shapes are created without repetition offsets,
        this can be added with this method
        """
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.repetitions = repetitions

    @abstractmethod
    def draw(self, draw):
        """
        draw

        Abstract method that should be implemented by the concrete classes
        """
        pass


class Rectangle(Shape):
    """
    Rentangle class.
    Concrete implementation of Shape, maps almost directly to
        -PIL.ImageDraw.ImageDraw.rectangle
    """

    def __str__(self):
        return "rectangle"

    def draw(self, draw):
        new_coord = self.coordinates
        for _ in range(0, self.repetitions):
            draw.rectangle(new_coord, self.color, self.outline)
            new_coord[0] += self.x_offset
            new_coord[1] += self.y_offset
            new_coord[2] += self.x_offset
            new_coord[3] += self.y_offset


class Ellipse(Shape):
    """
    Ellipse class.
    Concrete implementation of Shape, maps almost directly to
        -PIL.ImageDraw.ImageDraw.ellipse
    """

    def __str__(self):
        return "ellipse"

    def draw(self, draw):
        new_coord = self.coordinates
        # for ellipse, the final point has to be greater than the first
        if new_coord[0] > new_coord[2]:
            new_coord[0], new_coord[2] = new_coord[2], new_coord[0]
        if new_coord[1] > new_coord[3]:
            new_coord[1], new_coord[3] = new_coord[3], new_coord[1]
        for _ in range(0, self.repetitions):
            draw.ellipse(new_coord, self.color, self.outline)
            new_coord[0] += self.x_offset
            new_coord[1] += self.y_offset
            new_coord[2] += self.x_offset
            new_coord[3] += self.y_offset


class Circle(Shape):
    """
    Circle class.
    Concrete implementation of Shape, to
        -PIL.ImageDraw.ImageDraw.ellipse
    But with some modifications
    """

    def __str__(self):
        return "circle"

    def draw(self, draw):
        new_coord = self.coordinates
        # for circle, the last point is not a coordinate, is the size
        size = new_coord[2]
        new_coord[2] = new_coord[0]+size
        new_coord.append(new_coord[1]+size)

        for _ in range(0, self.repetitions):
            draw.ellipse(new_coord, self.color, self.outline)
            new_coord[0] += self.x_offset
            new_coord[1] += self.y_offset
            new_coord[2] += self.x_offset
            new_coord[3] += self.y_offset


class Polygon(Shape):
    """
    Ellipse class.
    Concrete implementation of Shape, maps almost directly to
        -PIL.ImageDraw.ImageDraw.polygon

    The number of points received (coordinates) is variable, but it
    should be an even number >= 6
    """

    def __str__(self):
        return "polygon"

    def draw(self, draw):
        new_coord = self.coordinates
        for _ in range(0, self.repetitions):
            draw.polygon(new_coord, self.color, self.outline)
            for index, _ in enumerate(new_coord):
                if index % 2 == 0:
                    new_coord[index] += self.x_offset
                else:
                    new_coord[index] += self.y_offset

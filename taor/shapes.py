"""
Shapes module.
Contains the abstract class Shape and all its children
"""
from abc import ABCMeta
import cv2
import numpy as np


class BaseShape(object):
    """
    BaseShape class.
    Abstract class to represent a Shape to be drawn in an image.
        It has a (initial) coordinate, color and outline
    """
    __metaclass__ = ABCMeta

    def __init__(self, coordinates, color, outline=None, thickness=1):
        self.coordinates = np.array(coordinates)
        self.color = color
        self.outline = outline
        self.thickness = thickness

    @staticmethod
    def validate_cc(component):
        """validate a color component"""
        # return component % 256
        return min(max(component, 0), 255)


class SimpleShape(BaseShape):
    """
    SimpleShape class.
    Abstract class to represent a simple Shape:
        Polygon, Rectangle, Ellipse.
        They can have X and/or Y repetition
    """
    __metaclass__ = ABCMeta

    def __init__(self, coordinates, color, outline=None, thickness=1):
        self.x_offset = 0
        self.y_offset = 0
        self.repetitions = 1
        super().__init__(coordinates, color, outline=outline, thickness=thickness)

    def set_repetition(self, x_offset, y_offset, repetitions):
        """
        set_repetition

        Shapes are created without repetition offsets,
        this can be added with this method
        """
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.repetitions = repetitions


class Rectangle(SimpleShape):
    """
    Rentangle class.
    Concrete implementation of Shape, maps almost directly to
        -cv2.rectangle
    """
    def __str__(self):
        return "rectangle"

    def draw(self, img):
        coord = self.coordinates
        for _ in range(0, self.repetitions):
            cv2.rectangle(img, tuple(coord[0:2]), tuple(coord[2:4]), self.color, -1)
            if self.outline:
                cv2.rectangle(
                    img, tuple(coord[0:2]), tuple(coord[2:4]),self.outline, self.thickness
                )
            coord += self.x_offset


class Ellipse(SimpleShape):
    """
    Ellipse class.
    Concrete implementation of Shape, maps to
        -cv2.ellipse
    """

    def __str__(self):
        return "ellipse"

    def draw(self, img):
        coord = self.coordinates
        for _ in range(0, self.repetitions):
            cv2.ellipse(img, tuple(coord[0:2]), tuple(coord[2:4]),
                        0, 0, 360, self.color, -1,)
            if self.outline:
                cv2.ellipse(img, tuple(coord[0:2]), tuple(coord[2:4]),
                            0, 0, 360, self.outline, self.thickness)
            coord[0:2] += self.x_offset


class Circle(SimpleShape):
    """
    Circle class.
    Concrete implementation of Shape, to
        -cv2.circle
    But with some modifications
    """

    def __str__(self):
        return "circle"

    def draw(self, img):
        coord = self.coordinates
        # for circle, the last point is not a coordinate, is the size
        size = coord[2]

        for _ in range(0, self.repetitions):
            cv2.circle(img, tuple(coord[0:2]), size, self.color, -1,)
            if self.outline:
                cv2.circle(
                    img, tuple(coord[0:2]), size, self.outline, self.thickness
                )
            coord[0:2] += self.x_offset


class Polygon(SimpleShape):
    """
    Polygon class.
    Concrete implementation of Shape, maps almost directly to
        -cv2.fillPoly

    The number of points received (coordinates) is variable, but it
    should be an even number >= 6 (three points, X and Y per each point)
    """

    def __str__(self):
        return "polygon"

    def draw(self, img):
        coord = self.coordinates
        for _ in range(0, self.repetitions):
            points = np.array([[tuple(coord[i:i + 2]) for i in range(0, len(coord), 2)]])
            cv2.fillPoly(img, points, self.color)
            for index, _ in enumerate(coord):
                if index % 2 == 0:
                    coord[index] += self.x_offset
                else:
                    coord[index] += self.y_offset

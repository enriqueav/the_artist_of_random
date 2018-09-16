import numpy as np
from taor.shapes import BaseShape
from numpy.random import choice, randint


class Generator(BaseShape):
    def __init__(self, coordinates, color, outline=None):
        super().__init__(coordinates, color, outline=None)

        self.origin = coordinates
        self.paint_coordinates = coordinates

        # Use the color picked as outline instead of fill
        p_color_as_outline = [0.85, 0.15]
        if choice([False, True], p=p_color_as_outline):
            self.color = None
            self.outline = color

        self.s = {}
        self.s['s_shapes'] = ["rectangle", "circle"]
        self.s['p_shapes'] = [0.5, 0.5]

        # COLOR CHANGE
        self.s['change_color'] = choice([False, True], p=[0.6, 0.4])
        self.s['change_color_unison'] = choice([False, True], p=[0.85, 0.15])
        self.s['p_change_color_every_step'] = [0.7, 0.3]
        # COLOR JUMP
        self.s['change_color_jump_every_step'] = choice([True, False], p=[0.5, 0.5])
        self.s['min_color_jump'] = randint(0, 11)
        self.s['max_color_jump'] = randint(self.s['min_color_jump']+1, 41)
        self.s['color_jump'] = randint(self.s['min_color_jump'], self.s['max_color_jump'])

        # ALPHA
        self.s['change_alpha'] = choice([False, True], p=[0.6, 0.4])
        self.s['p_change_alpha_every_step'] = [0.8, 0.2]
        self.s['alpha_jump'] = randint(1, 41)

        # SIZE
        self.s['min_size'] = randint(1, 60)
        self.s['max_size'] = randint(self.s['min_size']+1, 80+1)
        self.s['size'] = randint(self.s['min_size'], self.s['max_size'])
        self.s['change_size_every_step'] = choice([False, True], p=[0.8, 0.2])

        # SHAKINESS: each iteration can be slightly off the original x, y
        self.s['use_shakiness'] = choice([False, True], p=[0.8, 0.2])
        self.s['shakiness'] = randint(1, self.s['size']+1)

        # DEBUG
        # pprint.pprint(self.s)

    def adjust_color(self, color):
        if not color:
            return

        nr, ng, nb, alpha = color
        if self.s['change_color']:
            jump = self.s['color_jump']
            if self.s['change_color_unison']:
                while not (nr+ng+nb == 0 or nr+ng+nb == 255*3):
                    delta = randint(-jump, jump+1)
                    nr = Generator.validate_cc(nr + delta)
                    ng = Generator.validate_cc(ng + delta)
                    nb = Generator.validate_cc(nb + delta)
            else:
                if choice([False, True], p=self.s['p_change_color_every_step']):
                    nr = Generator.validate_cc(nr + randint(-jump, jump + 1))
                if choice([False, True], p=self.s['p_change_color_every_step']):
                    ng = Generator.validate_cc(ng + randint(-jump, jump + 1))
                if choice([False, True], p=self.s['p_change_color_every_step']):
                    nb = Generator.validate_cc(nb + randint(-jump, jump + 1))

        if self.s['change_alpha']:
            if choice([False, True], p=self.s['p_change_alpha_every_step']):
                alpha = Generator.validate_cc(
                    alpha + randint(-self.s['alpha_jump'], self.s['alpha_jump'])
                )
        return nr, ng, nb, alpha

    def new_step(self, draw):
        # SHAKINESS
        x, y = self.coordinates
        if self.s['use_shakiness']:
            x += randint(-self.s['shakiness'], self.s['shakiness']+1)
            y += randint(-self.s['shakiness'], self.s['shakiness']+1)
        self.paint_coordinates = [x, y, x + self.s['size'], y + self.s['size']]

        if self.s['shape'] == "circle":
            draw.ellipse(self.paint_coordinates, self.color, self.outline)
        if self.s['shape'] == "rectangle":
            draw.rectangle(self.paint_coordinates, self.color, self.outline)

        # CHANGE COLOR
        self.color = self.adjust_color(self.color)
        self.outline = self.adjust_color(self.outline)

        # CHANGE SIZE
        if self.s['change_size_every_step']:
            self.s['size'] = randint(self.s['min_size'], self.s['max_size'])

    @classmethod
    def get_delta(cls, direction):
        if direction == 0:
            delta = [-1, -1]
        elif direction == 1:
            delta = [0, -1]
        elif direction == 2:
            delta = [1, -1]
        elif direction == 3:
            delta = [1, 0]
        elif direction == 4:
            delta = [1, 1]
        elif direction == 5:
            delta = [0, 1]
        elif direction == 6:
            delta = [-1, 1]
        elif direction == 7:
            delta = [-1, 0]
        else:
            print("shapes.stain error, wrong direction %d" % direction)
            exit(0)
        return delta


class Lasso(Generator):
    """
    Lasso class. Experimental
    """
    def __init__(self, coordinates, color, outline=None):
        super().__init__(coordinates, color, outline=outline)

        self.s['quantity'] = randint(100, 10000)

        self.s['p_shapes'] = [0.5, 0.5]
        self.s['shape'] = choice(self.s['s_shapes'], p=self.s['p_shapes'])

        self.s['max_space_jump'] = randint(1, 61)
        self.s['space_jump'] = randint(1, self.s['max_space_jump']+1)
        self.s['change_space_jump_every_step'] = choice([False, True], p=[0.7, 0.3])

        craziness = int(np.sqrt(randint(2**2, 20**2)))
        p_no_change = 1 - (craziness/100)
        remaining = 1 - p_no_change
        p_1d = np.float(round(remaining*0.4, 3))
        p_2d = np.float(round(remaining*0.3, 3))
        p_3d = np.float(round(remaining*0.3, 3))
        p_no_change = 1 - p_1d - p_2d - p_3d
        self.s['p_change_direction'] = [p_no_change, p_1d, p_2d, p_3d]
        self.s['s_change_direction'] = [0, 1, 2, 3]
        self.s['max_grade'] = 3
        self.s['change_grade'] = randint(-self.s['max_grade'], self.s['max_grade']+1)

        # initial state
        self.s['direction'] = randint(0, 360)

    def draw(self, draw):
        for _ in range(self.s['quantity']):
            self.new_step(draw)

            delta = [
                np.cos(np.radians(self.s['direction'])),
                np.sin(np.radians(self.s['direction'])),
            ]

            if self.s['change_space_jump_every_step']:
                self.s['space_jump'] = randint(1, self.s['max_space_jump']+1)

            delta_grade = choice(self.s['s_change_direction'],
                                 p=self.s['p_change_direction'])
            delta_grade *= choice([-1, 1])
            self.s['change_grade'] = self.s['change_grade'] + delta_grade
            self.s['direction'] = (self.s['direction'] + (self.s['change_grade']/4))

            self.coordinates[0] += delta[0] * self.s['space_jump']
            self.coordinates[1] += delta[1] * self.s['space_jump']


class Explosion(Generator):
    """
    Explosion class. Experimental
    """
    def __init__(self, coordinates, color, outline=None):
        super().__init__(coordinates, color, outline=outline)
        self.s['quantity'] = randint(100, 10000)
        self.s['p_shapes'] = [0.4, 0.6]
        self.s['shape'] = choice(self.s['s_shapes'], p=self.s['p_shapes'])
        # ANGLE
        self.s['max_angle_jump'] = randint(1, 61)
        self.s['change_angle_jump_every_step'] = choice([False, True], p=[0.7, 0.3])
        self.s['angle_sign'] = choice([-1, 1])

        # DISTANCE FROM ORIGIN
        self.s['distance_jump'] = randint(1, 5)

        # initialized now, may be or may not be updated every step
        self.s['angle_jump'] = randint(1, self.s['max_angle_jump'] + 1)
        self.direction = randint(0, 360)
        self.distance = choice([0, randint(1, 100)])

    def draw(self, draw):
        for _ in range(self.s['quantity']):
            self.new_step(draw)

            if self.s['change_angle_jump_every_step']:
                self.s['angle_jump'] = randint(1, self.s['max_angle_jump']+1)

            self.direction += (self.s['angle_jump']*self.s['angle_sign'])
            delta = [
                np.cos(np.radians(self.direction)),
                np.sin(np.radians(self.direction)),
            ]

            self.distance = self.distance + self.s['distance_jump']
            self.coordinates[0] = self.origin[0] + (delta[0] * self.distance)
            self.coordinates[1] = self.origin[1] + (delta[1] * self.distance)


class StainGrid(Generator):
    """
    StainGrid class. Experimental
    """
    def __init__(self, coordinates, color, outline=None):
        super().__init__(coordinates, color, outline=outline)
        self.s['quantity'] = randint(1000, 100000)
        self.s['shape'] = choice(self.s['s_shapes'], p=[0.6, 0.4])
        self.s['size'] = randint(2, 31)
        self.s['space_jump'] = randint(1, self.s['size']*4)
        # pprint.pprint(self.s)

    def draw(self, draw):
        for _ in range(self.s['quantity']):
            self.new_step(draw)
            direction = randint(0, 8)
            delta = Generator.get_delta(direction)
            self.coordinates[0] += delta[0] * self.s['space_jump']
            self.coordinates[1] += delta[1] * self.s['space_jump']


class Worm(Generator):
    """
    Worm class. Experimental
    """
    def __init__(self, coordinates, color, outline=None):
        super().__init__(coordinates, color, outline=outline)
        self.s['quantity'] = randint(1000, 10000)
        self.s['p_shapes'] = [0.5, 0.5]
        self.s['shape'] = choice(self.s['s_shapes'], p=self.s['p_shapes'])
        self.s['size'] = randint(2, 41)

        craziness = int(np.sqrt(randint(1, 8**2)))
        p_no_change = 1 - (craziness/100)
        remaining = 1 - p_no_change
        p_1d = np.float(round(remaining*0.5, 3))
        p_2d = np.float(round(remaining*0.3, 3))
        p_3d = np.float(round(remaining*0.2, 3))
        p_no_change = 1 - p_1d - p_2d - p_3d
        self.s['p_change_direction'] = [p_no_change, p_1d, p_2d, p_3d]
        self.s['s_change_direction'] = [0, 1, 2, 3]
        self.s['max_space_jump'] = randint(1, self.s['size']*2)
        self.s['change_space_jump_every_step'] = choice([False, True], p=[0.8, 0.2])

        # init
        self.s['space_jump'] = randint(1, self.s['max_space_jump']+1)
        self.direction = randint(0, 8)
        # pprint.pprint(self.s)

    def __str__(self):
        return "stain"

    def draw(self, draw):
        for _ in range(self.s['quantity']):
            self.new_step(draw)

            delta = choice(self.s['s_change_direction'],
                           p=self.s['p_change_direction'])
            delta *= choice([-1, 1])
            self.direction = (self.direction + delta) % 8
            delta = Generator.get_delta(self.direction)

            if self.s['change_space_jump_every_step']:
                self.s['space_jump'] = randint(1, self.s['max_space_jump']+1)

            self.coordinates[0] += delta[0] * self.s['space_jump']
            self.coordinates[1] += delta[1] * self.s['space_jump']

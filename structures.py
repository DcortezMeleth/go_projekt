# -*- coding: UTF-8 -*-

import graphics

__author__ = 'Bartosz'


# klasa reprezentująca punkt w przestrzeni
class Point(graphics.Point):
    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)



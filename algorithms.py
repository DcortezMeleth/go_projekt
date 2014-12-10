# -*- coding: UTF-8 -*-
import math
import graphics
import numpy as np
import structures as struct

__author__ = 'Bartosz'


# metoda licząca kąt pomiędzy punktami
def get_degree(base, target):
    angle = math.degrees(math.atan2(target.y - base.y, target.x - base.x))
    if angle < 0:
        angle += 360
    return angle


# metoda licząca kąt pomiędzy punktami dla odwróconej osi x
def get_degree_reverse(base, target):
    angle = math.degrees(math.atan2(target.y - base.y, base.x - target.x))
    if angle < 0:
        angle += 360
    return angle


# metoda licząca dystans pomiędzy punktami
def get_distance(base, target):
    return math.sqrt((base.x - target.x)**2 + (base.y - target.y)**2)


# wyszukuje w liście punkt o najmniejszym y
def find_lowest_y(points):
    lowest = points[0]
    for point in points:
        if point.y < lowest.y or point.y == lowest.y and point.x < lowest.x:
            lowest = point
    return lowest


# wyszukuje w liście punkt o największym y
def find_highest_y(points):
    highest = points[0]
    for point in points:
        if point.y > highest.y or point.y == highest.y and point.x < highest.x:
            highest = point
    return highest


# sprawdza czy punkt z leży na lewo od odcinka [x,y]
def is_left(x, y, z):
    alpha = get_degree(x, y)
    beta = get_degree(x, z)
    return alpha < beta < alpha + 180


def comparator(tmp, x1, x2):
    if x1 == tmp:
        return x2
    if x2 == tmp:
        return x1
    if get_degree(tmp, x1) == get_degree(tmp, x2):
        return x1 if get_distance(tmp, x1) > get_distance(tmp, x2) else x2
    return x1 if get_degree(tmp, x1) < get_degree(tmp, x2) else x2


def reverse_comparator(tmp, x1, x2):
    if x1 == tmp:
        return x2
    if x2 == tmp:
        return x1
    if get_degree_reverse(tmp, x1) == get_degree_reverse(tmp, x2):
        return x1 if get_distance(tmp, x1) > get_distance(tmp, x2) else x2
    return x1 if get_degree_reverse(tmp, x1) < get_degree_reverse(tmp, x2) else x2


def get_angle(p0, p1, p2):
    ''' compute angle (in degrees) for p0p1p2 corner
    Inputs:
        p0,p1,p2 - points in the form of [x,y]
    '''
    p0 = [p0.x, p0.y]
    p1 = [p1.x, p1.y]
    p2 = [p2.x, p2.y]
    v1 = np.array(p0) - np.array(p1)
    v0 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    return abs(np.degrees(angle))


def draw_circle(win, points):
    if len(points) == 3:
        x = complex(points[0].x, points[0].y)
        y = complex(points[1].x, points[1].y)
        z = complex(points[2].x, points[2].y)
        w = z - x
        w /= y - x
        c = (x - y)*(w - abs(w)**2)/2j/w.imag - x
        print '(x%+.3f)^2+(y%+.3f)^2=%.3f^2' % (c.real, c.imag, abs(c + x))
        circle = graphics.Circle(graphics.Point(-c.real, -c.imag), abs(c+x))
    else:
        dx = (points[0].x - points[1].x)/2
        dy = (points[0].y - points[1].y)/2
        center = struct.Point(points[1].x + dx, points[1].y + dy)
        radius = math.sqrt(dx**2 + dy**2)
        circle = graphics.Circle(center, radius)
        print '(x%+.3f)^2+(y%+.3f)^2=%.3f^2' % (-center.x, -center.y, radius)
    circle.draw(win)


class Graham(object):
    def __init__(self, points):
        self._points = points
        self._p0 = find_lowest_y(points)
        self._result = []

    def solve(self):
        if len(self._points) < 3:
            return None

        # krok pierwszy - wybieramy p0 - zrobione w konstruktorze

        # krok drugi - sortowanie punktów
        sorted_points = sorted(self._points, key=lambda x: (get_degree(self._p0, x), -get_distance(self._p0, x)))
        result = [sorted_points[0]]
        for point in sorted_points[1:]:
            if get_degree(self._p0, point) != get_degree(self._p0, result[-1]):
                result.append(point)

        # krok trzeci - definiujemy stos
        self._result = result[:3]

        # krok czwarty - szukanie rozwiązania
        i = 3
        while i < len(result):
            if is_left(self._result[-2], self._result[-1], result[i]):
                self._result.append(result[i])
                i += 1
            else:
                self._result.pop()

    def get_result(self):
        return self._result


class Applet(object):
    def __init__(self, points):
        self._points = points
        graham = Graham(points)
        graham.solve()
        self._hull = graham.get_result()
        self._result = []

    def solve(self):
        if len(self._hull) < 3:
            return self._hull
        win = graphics.GraphWin("go_projekt", 800, 600)
        for p in self._points:
            p.draw(win)
        self._result = self.inner_solve(self._hull[0], self._hull[1], win)
        draw_circle(win, self._result)
        win.getMouse()
        win.close()

    def inner_solve(self, p1, p2, win):
        new_list = list(self._hull)
        new_list.remove(p1)
        new_list.remove(p2)
        f = lambda x, y: x if get_angle(p1, x, p2) < get_angle(p1, y, p2) else y
        best = reduce(f, new_list)
        triangle = graphics.Polygon(p1, p2, best)
        triangle.draw(win)
        win.getMouse()
        triangle.undraw()
        if get_angle(p1, best, p2) >= 90:
            return [p1, p2]
        alpha = get_angle(p1, p2, best)
        beta = get_angle(p2, p1, best)
        if alpha > 90:
            return self.inner_solve(p1, best, win)
        if beta > 90:
            return self.inner_solve(p2, best, win)
        return [p1, p2, best]


class MinimumArea(object):
    def __init__(self, points):
        self._points = points
        graham = Graham(points)
        graham.solve()
        self._hull = graham.get_result()
        self._hull = self._hull[::-1]
        self._hull.append(self._hull[0])
        self._min_area = None
        self._min_perimeter = None

    def most_far(self, j, sin, cos, mx, my):
        n = len(self._hull)
        xn, yn = self._hull[j].x, self._hull[j].y
        rx, ry = xn*cos - yn*sin, xn*sin + yn*cos
        best = mx*rx + my*ry
        while True:
            x, y = rx, ry
            xn, yn = self._hull[(j + 1) % n].x, self._hull[(j + 1) % n].y
            rx, ry = xn*cos - yn*sin, xn*sin + yn*cos
            if mx*rx + my*ry >= best:
                j = (j + 1) % n
                best = mx*rx + my*ry
            else:
                return x, y, j

    def solve(self):
        i_l = i_r = i_p = 1  # indeksy: lewy, prawy, przeciwny
        min_area = (1e33, 0, 0, 0, 0, 0)
        min_perimeter = (1e33, 0, 0, 0, 0, 0)
        for i in xrange(len(self._hull) - 1):
            dx = self._hull[i + 1].x - self._hull[i].x
            dy = self._hull[i + 1].y - self._hull[i].y
            theta = math.pi - math.atan2(dy, dx)
            sin, cos = math.sin(theta), math.cos(theta)
            y_c = self._hull[i].x*sin + self._hull[i].y*cos

            x_p, y_p, i_p = self.most_far(i_p, sin, cos, 0, 1)
            if i == 0:
                i_r = i_p
            x_r, y_r, i_r = self.most_far(i_r, sin, cos, 1, 0)
            x_l, y_l, i_l = self.most_far(i_l, sin, cos, -1, 0)
            area = (y_p - y_c)*(x_r - x_l)
            perimeter = 2*((y_p - y_c) + (x_r - x_l))

            print i, area, perimeter, (y_p - y_c), (x_r - x_l), y_p, y_c, x_r, x_l

            if area < min_area[0]:
                min_area = (area, x_r - x_l, y_p - y_c, i, i_l, i_p, i_r)
            if perimeter < min_perimeter[0]:
                min_perimeter = (perimeter, x_r - x_l, y_p - y_c, i, i_l, i_p, i_r)

        self._min_area = min_area
        self._min_perimeter = min_perimeter
        print min_area
        print min_perimeter

    def get_min_area(self):
        return self._min_area

    def get_min_perimeter(self):
        return self._min_perimeter

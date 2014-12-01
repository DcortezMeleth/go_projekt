# -*- coding: UTF-8 -*-
import math

import graphics


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
    return math.sqrt((base.x - target.x) ** 2 + (base.y - target.y) ** 2)


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


def get_angle(x, y, z):
    angle = abs(math.degrees(math.atan2(x.getY() - z.getY(), x.getX() - z.getX())
                             - math.atan2(y.getY() - z.getY(), y.getX() - z.getX())))
    if angle > 180:
        angle -= 180
    return angle


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


class Jarvis(object):
    def __init__(self, points):
        self._points = points
        self._p0 = find_lowest_y(points)
        self._p1 = find_highest_y(points)
        self._result = []

    def solve(self):
        if len(self._points) < 3:
            return None

        # prawa strona otoczki
        tmp = self._p0
        self._result.append(self._p0)
        while tmp != self._p1:
            f = lambda x, y: comparator(tmp, x, y)
            best = reduce(f, self._points)
            # pierwszym elementem zawsze będzie nasz obecny punkt, bo mamy wtedy kąt 0 stopni
            self._result.append(best)
            tmp = self._result[-1]

        # lewa strona otoczki
        tmp = self._p0
        result = []
        while tmp != self._p1:
            f = lambda x, y: reverse_comparator(tmp, x, y)
            best = reduce(f, self._points)
            result.append(best)
            tmp = result[-1]

        # usuwamy p1, bo zostało dodane 2 razy
        result = result[:-1]

        self._result.extend(result[::-1])

    def get_result(self):
        return self._result


class Applet(object):
    def __init__(self, points):
        self._points = points
        jarvis = Jarvis(points)
        jarvis.solve()
        self._hull = jarvis.get_result()

    def solve(self):
        if len(self._hull) < 4:
            return self._hull
        return self.inner_solve(self._hull[0], self._hull[1])

    def inner_solve(self, p1, p2):
        new_list = list(self._hull)
        new_list.remove(p1)
        new_list.remove(p2)
        f = lambda x, y: x if get_angle(p1, p2, x) < get_angle(p1, p2, y) else y
        best = reduce(f, new_list)
        if get_angle(p1, p2, best) >= 90:
            return [p1, p2]
        alpha = get_angle(p1, best, p2)
        beta = get_angle(p2, best, p1)
        if alpha > 90:
            return self.inner_solve(p1, best)
        if beta > 90:
            return self.inner_solve(p2, best)
        return [p1, p2, best]


































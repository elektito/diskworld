from point import Point
from vector import Vector

class Camera(object):
    def __init__(self, bottomleft=None, topright=None, width=None, height=None):
        if bottomleft is not None and topright is not None:
            if not isinstance(bottomleft, Point) or not isinstance(topright, Point):
                raise ValueError("bottomleft and topright arguments must be Point instances.")

            if bottomleft.x >= topright.x or bottomleft.y >= topright.y:
                raise ValueError("Invalid coordinates for camera bottom-left/top-right.")

            self.__bottomleft = bottomleft
            self.__topright = topright

        elif bottomleft is not None and width is not None and height is not None:
            if not isinstance(bottomleft, Point):
                raise ValueError("bottomleft argument must be Point instances.")

            if width <= 0 or height <= 0:
                raise ValueError("Camera width and height cannot be negative.")

            self.__bottomleft = bottomleft
            self.__topright = Point(bottomleft.x + width, bottomleft.y + height)

        else:
            raise ValueError()

    @property
    def bottomleft(self):
        return self.__bottomleft

    @bottomleft.setter
    def bottomleft(self, value):
        raise AttributeError("Cannot set camera properties directly. Use pan and/or zoom instead.")

    @property
    def topright(self):
        return self.__topright

    @topright.setter
    def topright(self, value):
        raise AttributeError("Cannot set camera properties directly. Use pan and/or zoom instead.")

    @property
    def width(self):
        return float(self.topright.x - self.bottomleft.x)

    @width.setter
    def width(self, value):
        raise AttributeError("Cannot set camera properties directly. Use pan and/or zoom instead.")

    @property
    def height(self):
        return float(self.topright.y - self.bottomleft.y)

    @height.setter
    def height(self, value):
        raise AttributeError("Cannot set camera properties directly. Use pan and/or zoom instead.")

    @property
    def center(self):
        return self.bottomleft + Vector(self.width / 2.0, self.height / 2.0)

    @center.setter
    def center(self, value):
        raise AttributeError("Cannot set camera properties directly. Use pan and/or zoom instead.")

    def isInView(self, disk):
        distanceX = abs(disk.center.x - self.center.x)
        distanceY = abs(disk.center.y - self.center.y)

        if distanceX > self.width / 2 + disk.radius:
            return False

        if distanceY > self.height / 2 + disk.radius:
            return False

        if distanceX <= self.width / 2:
            return True

        if distanceY <= self.height / 2:
            return True

        cornerDistanceSq = (distanceX - self.width / 2) ** 2 + \
                           (distanceY - self.height / 2) ** 2
        return cornerDistanceSq <= disk.radius ** 2

    def zoom(self, z):
        '''Zooms the camera in or out by the specified amount. A positive
value for z means zoom in, a negative value zoom out. For example
calling camera.zoom(0.2) zooms the camera in for 20%, while
camera.zoom(-0.1) zooms the camera out for 10%.

        '''

        w, h = self.width, self.height
        nw = w * (1 - z)
        nh = nw * (h / w)

        self.__bottomleft = Point(self.bottomleft.x - (nw - w) / 2,
                                  self.bottomleft.y - (nh - h) / 2)
        self.__topright = Point(self.topright.x + (nw - w) / 2,
                                self.topright.y + (nh - h) / 2)

    def pan(self, v):
        '''Pans the camera with the amount specified by the vector v. As an
example, camera.pan(Vector(3, -8) pans the camera three meters to the
right and eight meter downwards.

        '''

        self.__bottomleft += v
        self.__topright += v

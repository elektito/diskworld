from point import Point

class Camera:
    def __init__(self, x1, y1, x2, y2):
        '''Defines a canera that views a rectangle with (x1, y1) as its
bottom-left and (x2, y2) as its top-right.'''

        if x1 >= x2 or y1 >= y2:
            raise ValueError('x1({}) needs to be smaller than x2({}) and y1({}) needs to be smaller than y2({}).'.format(
                x1, x2, y1, y2))

        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def center(self):
        return Point(self.x1 + self.width / 2.0,
                     self.y1 + self.height / 2.0)

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

        nw = self.width * (1 - z)
        w, h = self.width, self.height
        nh = nw * (h / w)
        self.x1 -= (nw - w) / 2
        self.x2 += (nw - w) / 2
        self.y1 -= (nh - h) / 2
        self.y2 += (nh - h) / 2

    def pan(self, v):
        '''Pans the camera with the amount specified by the vector v. As an
example, camera.pan(Vector(3, -8) pans the camera three meters to the
right and eight meter downwards.

        '''

        bl = Point(self.x1, self.y1)
        tr = Point(self.x2, self.y2)
        bl += v
        tr += v
        self.x1, self.y1 = bl.x, bl.y
        self.x2, self.y2 = tr.x, tr.y

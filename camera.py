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

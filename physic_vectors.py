from vector import Vector


class Velocity(Vector):
    ''' 2D velocity vector '''

    ''' speed of light m/s '''
    c = 299792458

    def __init__(self, x, y):
        super().__init__(x, y)
        if self.norm() > Velocity.c:
            raise FasterThanLightError(
                f'Velocity {self.norm()} m/s is faster than light!')

    def __eq__(self, other):
        return True if self.values == other.values else False


class Position(Vector):

    def __init__(self, x, y):
        super().__init__(x, y)

    def __eq__(self, other):
        return True if self.values == other.values else False


class FasterThanLightError(Exception):
    def __init__(self, msg, point_object=None):
        super().__init__(msg)
        self.point_object = point_object
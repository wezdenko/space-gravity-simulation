from physic_vectors import Velocity, Position
from physic_units import Mass, Radius

gravity_const = 6.674 * 10**(-11)
light_speed = 3 * 10**8


class Object:
    '''
    This class represents an physical object and it
    exists so classes PointObject and CentralObject
    can inherit from it.

    Attributes:
    -position (Position object)
    -velocity (Velocity object)
    -mass
    -radius
    '''

    num_objects = 0

    def __init__(self, position, velocity, mass, radius):
        self._position = position
        self._velocity = velocity
        self._mass = mass
        self._radius = radius

        Object.num_objects += 1

    @property
    def x_axis(self):
        return self._position[0]

    @property
    def y_axis(self):
        return self._position[1]

    def check_distance(self, other):
        '''returns distance (float or int) between two objects '''
        return (other._position - self._position).norm()

    def distance_vector(self, other):
        '''returns distance vector between two objects '''
        return other._position - self._position

    def check_pixel(self, scale):
        '''checks which pixel object is located on and returns
        tuple (x, y) - coordinates of the pixel '''
        if scale <= 0:
            raise ValueError(f'Scale must have positive value: {scale}')
        return (int(self.x_axis / scale), int(self.y_axis / scale))

    def check_if_inside_img(self, size, scale):
        '''bool method, returns True if object is inside image,
        size - size of an image (positive int)
        scale - scale of an image (positive float) '''
        if type(size) != int or size <= 0:
            raise ValueError(f'Size must be a positive intiger: {size}')
        if 0 <= self.check_pixel(scale)[0] < size:
            if 0 <= self.check_pixel(scale)[1] < size:
                return True
        return False


class PointObject(Object):

    '''
    Represents an object without mass and with no radius.

    Attributes:
    -position (Position object)
    -velocity (Velocity object)
    '''

    num_pointobjects = 0

    def __init__(self, position=Position(0, 0), velocity=Velocity(0, 0)):
        super().__init__(position, velocity, 0, 0)

        PointObject.num_pointobjects += 1

    def calculate_velocity(self, central_obj, time):
        '''returns a float value (velocity) of the point object
        which is gravitationally pulled by a central object '''
        distance = self.check_distance(central_obj)
        return gravity_const * central_obj._mass * time / distance**2

    def update_velocity(self, central_obj, time):
        '''calculates and sets velocity attribute after given time '''
        velocity = self.calculate_velocity(central_obj, time)
        distance_vector = self.distance_vector(central_obj)
        self._velocity += velocity * distance_vector.normalize()

    def update_position(self, time):
        '''takes velocity attribute and moves object to another
        position in given time '''
        self._position += self._velocity * float(time)

    def is_on_same_pixel(self, other, scale):
        '''bool function, returns True if two objects are on the
        same pixel'''
        if self.check_pixel(scale) == other.check_pixel(scale):
            return True
        return False


class CentralObject(Object):

    '''
    Represents a massive, imovable object.

    Attributes:
    -mass
    -radius
    -position (Position object)
    '''

    earth_mass = 6 * 10**24
    earth_radius = 6371000

    def __init__(self, mass=Mass(earth_mass), radius=Radius(earth_radius),
                 position=Position(0, 0)):
        super().__init__(position, Velocity(0, 0), mass, radius)

        if self.schwarzschild_radius() > self._radius:
            raise TooSmallRadiusError(
                f'Miniman radius can be {self.schwarzschild_radius()}')

    def schwarzschild_radius(self):
        '''returns minimal radius object can have as a black hole'''
        print(self._mass)
        return 2 * gravity_const * self._mass / light_speed**2

    def is_inside_radius(self, pixel, scale):
        '''bool function, returns True if pixel is inside radius
        -pixel - tuple (x, y)'''
        x, y = self.check_pixel(scale)
        radius = self.pixel_radius(scale)
        condition = (pixel[0] - x)**2 + (pixel[1] - y)**2
        if condition < radius**2:
            return True
        return False

    def pixel_radius(self, scale):
        '''returns lenght of the radius in pixels'''
        return int(self._radius / scale)


class TooSmallRadiusError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


if __name__ == '__main__':
    c_obj = CentralObject(10**24)
    p_obj = PointObject(Position(10**7, 0))

    p1 = PointObject(Position(-3, -4))
    p2 = PointObject(Position(0, 0))
    p3 = PointObject(Position(30, 100.0009))

    print(p3.check_pixel(10))

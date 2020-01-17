from sim_image import SimImage
from objects import PointObject, CentralObject, TooSmallRadiusError
from physic_vectors import Velocity, Position, FasterThanLightError
from physic_units import Size, Scale, Steps, Time, Mass, Radius


def _number_input(msg, number_type=float):
    try:
        return number_type(input(msg))
    except ValueError:
        raise InputError('This value must be a number!')


def image_input():
    return SimImage(_size_input(), _scale_input())


def _size_input():
    try:
        value = _number_input('Type in size of the image: ', int)
        return Size(value)
    except (ValueError, TypeError, InputError) as e:
        print(e)
        return _size_input()


def _scale_input():
    try:
        value = _number_input('Type in scale of the image: ')
        return Scale(value)
    except (ValueError, TypeError, InputError) as e:
        print(e)
        return _scale_input()


def steps_input():
    try:
        value = _number_input('Type in number of steps in simulation: ', int)
        return Steps(value)
    except (ValueError, TypeError, InputError) as e:
        print(e)
        return steps_input()


def time_input():
    try:
        value = _number_input('Type in time per step: ')
        return Time(value)
    except (ValueError, TypeError, InputError) as e:
        print(e)
        return time_input()


def central_object_input():
    print('Type in attributes of the central object: ')
    try:
        return CentralObject(
            position=_position_input(),
            mass=_mass_input(),
            radius=_radius_input()
        )
    except TooSmallRadiusError as e:
        print(e)
        return central_object_input()


def _mass_input():
    try:
        value = _number_input('Type in mass of the central object: ')
        print(Mass(value))
        return Mass(value)
    except (ValueError, TypeError, InputError) as e:
        print(e)
        return _mass_input()


def _radius_input():
    try:
        value = _number_input('Type in radius of the central object: ')
        return Radius(value)
    except (ValueError, TypeError, InputError) as e:
        print(e)
        return _radius_input()


def point_objects_list_input():
    try:
        i = _number_input('Type in number of point objects: ', int)
        if i < 0:
            raise ValueError('Number of point objects can\'t be negative!')
    except (ValueError, InputError) as e:
        print(e)
        return point_objects_list_input()
    objects_list = []
    for i in range(i):
        objects_list.append(_point_object_input())
    return objects_list


def _point_object_input():
    return PointObject(
        position=_position_input(),
        velocity=_velocity_input()
    )


def _position_input():
    print(4*' '+'Type in values of the position vector: ')
    try:
        x = _number_input(8*' '+'x value: ')
        y = _number_input(8*' '+'y value: ')
        return Position(x, y)
    except (ValueError, TypeError, InputError) as e:
        print(e)
        return _position_input()


def _velocity_input():
    print(4*' '+'Type in values of the velocity vector: ')
    try:
        x = _number_input(8*' '+'x value: ')
        y = _number_input(8*' '+'y value: ')
        return Velocity(x, y)
    except (ValueError, TypeError, FasterThanLightError, InputError) as e:
        print(e)
        return _velocity_input()


class InputError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

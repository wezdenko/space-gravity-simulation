from objects import PointObject, CentralObject
from physic_vectors import Velocity, Position

'''central object with 10^24 kg mass located on [0, 0]'''
c_obj = CentralObject(10**24)

'''point object located on [10^7, 0] with 0 velocity'''
p_obj = PointObject(Position(10**7, 0))


'''Tests for class Object'''


def test_check_distance():
    p_obj_1 = PointObject(Position(3, 4))
    p_obj_2 = PointObject(Position(6, 8))
    p_obj_3 = PointObject(Position(0, 0))

    assert p_obj.check_distance(c_obj) == 10**7
    assert p_obj_1.check_distance(p_obj_2) == 5
    assert p_obj_3.check_distance(p_obj_2) == 10
    assert p_obj_3.check_distance(c_obj) == 0


def test_distance_vector():
    p_obj_1 = PointObject(Position(3, 4))
    p_obj_2 = PointObject(Position(6, 8))
    p_obj_3 = PointObject(Position(0, 0))

    assert p_obj.distance_vector(c_obj) == Position(-10**7, 0)
    assert p_obj_1.distance_vector(p_obj_2) == Position(3, 4)
    assert p_obj_3.distance_vector(p_obj_2) == Position(6, 8)
    assert p_obj_3.distance_vector(c_obj) == Position(0, 0)


def test_check_pixel():
    p_obj_1 = PointObject(Position(30, 40))
    p_obj_2 = PointObject(Position(3.1415, 9.9238))
    p_obj_3 = PointObject(Position(0, 0))
    p_obj_4 = PointObject(Position(-3, -2))
    p_obj_5 = PointObject(Position(-0.1, -0.1))

    assert p_obj_1.check_pixel(10) == (3, 4)
    assert p_obj_2.check_pixel(1) == (3, 9)
    assert p_obj_3.check_pixel(1234) == (0, 0)
    assert p_obj_4.check_pixel(1) == (-3, -2)
    assert p_obj_5.check_pixel(1) == (-1, -1)


def test_check_if_inside_img():
    p_obj_1 = PointObject(Position(30, 40))
    p_obj_2 = PointObject(Position(30, 39.99999))
    p_obj_3 = PointObject(Position(-2, -1))
    p_obj_4 = PointObject(Position(0, 0))

    assert p_obj_1.check_if_inside_img(10, 100) is True
    assert p_obj_1.check_if_inside_img(10, 4) is False
    assert p_obj_2.check_if_inside_img(10, 4) is True
    assert p_obj_3.check_if_inside_img(10, 1) is False
    assert p_obj_4.check_if_inside_img(10, 1) is True


'''Tests for class PointObject'''


def test_calculate_velocity():
    p_obj.calculate_velocity(c_obj, 1) == -0.6674


def test_update_velocity():
    p_obj.update_velocity(c_obj, 1)

    assert round(p_obj._velocity[0], 4) == -0.6674
    assert p_obj._velocity[1] == 0


def test_update_position():
    p_obj_1 = PointObject(Position(0, 0), Velocity(0, 0))
    p_obj_2 = PointObject(Position(0, 0), Velocity(10, 10))
    p_obj_3 = PointObject(Position(0, 0), Velocity(-10, -10))

    p_obj_1.update_position(0)
    assert p_obj_1._position == Position(0, 0)

    p_obj_1.update_position(5)
    assert p_obj_1._position == Position(0, 0)

    p_obj_2.update_position(1)
    assert p_obj_2._position == Position(10, 10)

    p_obj_2.update_position(5)
    assert p_obj_2._position == Position(60, 60)

    p_obj_3.update_position(2)
    assert p_obj_3._position == Position(-20, -20)


def test_is_on_same_pixel():
    p_obj_1 = PointObject(Position(30, 40))
    p_obj_2 = PointObject(Position(30, 39.99999))
    p_obj_3 = PointObject(Position(30.999, 40.123))
    p_obj_4 = PointObject(Position(-3.001, -1))
    p_obj_5 = PointObject(Position(-4, -0.1))

    assert p_obj_1.is_on_same_pixel(p_obj_2, 10) is False
    assert p_obj_1.is_on_same_pixel(p_obj_3, 10) is True
    assert p_obj_4.is_on_same_pixel(p_obj_5, 1) is True
    assert p_obj_4.is_on_same_pixel(p_obj_5, 0.5) is False


'''Tests for class CentralObject'''


def test_pixel_radius():
    c_obj_1 = CentralObject(radius=100)
    c_obj_2 = CentralObject(radius=999)

    c_obj_1.pixel_radius(10) == 10
    c_obj_2.pixel_radius(100) == 99


def test_schwarzschild_radius():
    c_obj_1 = CentralObject(mass=5.97*10**24)

    assert round(c_obj_1.schwarzschild_radius(), 5) == 0.00885

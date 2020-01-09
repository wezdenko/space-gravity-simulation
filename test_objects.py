from objects import PointObject, CentralObject
from physic_vectors import Velocity, Position

'''central object with 10^24 kg mass located on [0, 0]'''
c_obj = CentralObject(10**24)

'''point object located on [10^7, 0] with 0 velocity'''
p_obj = PointObject(Position(10**7, 0))


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


def test_update_velocity():
    p_obj.update_velocity(c_obj, 1)

    assert p_obj._velocity == Velocity(-0.6674, 0)


def test_update_position():
    pass


def test_check_pixel():
    p_obj_1 = PointObject(Position(30, 40))
    p_obj_2 = PointObject(Position(3.1415, 9.9238))
    p_obj_3 = PointObject(Position(0, 0))
    p_obj_4 = PointObject(Position(-3, -2))

    assert p_obj_1.check_pixel(10) == (3, 4)
    assert p_obj_2.check_pixel(1) == (3, 9)
    assert p_obj_3.check_pixel(1234) == (0, 0)
    assert p_obj_4.check_pixel(1) == (-3, -2)


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

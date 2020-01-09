from physic_vectors import Velocity, Position

v1 = Velocity(3, 4)
v2 = Velocity(12, 16)
v3 = Velocity(0, 0)
v4 = Velocity(-3, -4)


def test_value():
    assert v1.value() == 5
    assert v2.value() == 20
    assert v3.value() == 0
    assert v4.value() == 5

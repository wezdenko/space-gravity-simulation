from physic_vectors import Velocity, Position, FasterThanLightError
import pytest

v2 = Velocity(12, 16)
v3 = Velocity(0, 0)
v4 = Velocity(-3, -4)


def test_type_error():
    with pytest.raises(TypeError):
        Velocity('a', 1)
        Position('b', 'da')

def test_faster_than_light_error():
    with pytest.raises(FasterThanLightError):
        Velocity(3*10**8, 0)

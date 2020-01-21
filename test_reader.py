import json
from reader import (ImageReader, SimulationReader, CentralObjectReader,
                    PointObjectReader, PositionReader, VelocityReader)
from physic_vectors import Position, Velocity


save = json.dumps({
            "image": {
                "size": 101,
                "scale": 200000
            },
            "steps": 3000,
            "time_per_step": 2,
            "central_object": {
                "mass": 6000000000000000000000000,
                "radius": 3371000,
                "position": {
                    "x": 10100000,
                    "y": 10100000
                }
            },
            "point_objects_list": [{
                "point_object": {
                    "position": {
                        "x": 10100000,
                        "y": 3058000
                    },
                    "velocity": {
                        "x": 7540,
                        "y": 0
                    }
                }
            }, {
                "point_object": {
                    "position": {
                        "x": 10100000,
                        "y": 2058000
                    },
                    "velocity": {
                        "x": -4540,
                        "y": 0
                    }
                }
            }]
        })


def test_image_reader():
    image = ImageReader(save).read()

    assert image.size == 101
    assert image.scale == 200000


def test_simulation_reader():
    steps = SimulationReader(save).read_steps()
    time_per_step = SimulationReader(save).read_time()

    steps == 3000
    time_per_step == 2


def test_position_reader():
    position_0 = PositionReader(json.loads(save)).read()
    position_1 = PositionReader(json.loads(save), 0).read()
    position_2 = PositionReader(json.loads(save), 1).read()

    assert position_0 == Position(10100000, 10100000)
    assert position_1 == Position(10100000, 3058000)
    assert position_2 == Position(10100000, 2058000)


def test_velocity_reader():
    velocity_0 = VelocityReader(json.loads(save), 0).read()
    velocity_1 = VelocityReader(json.loads(save), 1).read()

    assert velocity_0 == Velocity(7540, 0)
    assert velocity_1 == Velocity(-4540, 0)


def test_central_object_reader():
    central_object = CentralObjectReader(save).read()

    assert central_object.x_axis == 10100000
    assert central_object.y_axis == 10100000
    assert central_object._mass == 6e+24
    assert central_object._radius == 3371000


def test_point_object_reader():
    point_object_0 = PointObjectReader(json.loads(save), 0).read()
    point_object_1 = PointObjectReader(json.loads(save), 1).read()

    assert point_object_0.x_axis == 10100000
    assert point_object_0.y_axis == 3058000
    assert point_object_0._velocity[0] == 7540
    assert point_object_0._velocity[1] == 0

    assert point_object_1.x_axis == 10100000
    assert point_object_1.y_axis == 2058000
    assert point_object_1._velocity[0] == -4540
    assert point_object_1._velocity[1] == 0

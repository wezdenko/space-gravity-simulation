from PIL import Image
from sim_image import SimImage
from objects import PointObject, CentralObject, TooSmallRadiusError
from physic_vectors import Velocity, Position, FasterThanLightError
white = (255, 255, 255)
import json


def read(lines, line_num, column, data_type=int):
    try:
        data = lines[line_num].strip().split(',')
    except IndexError:
        raise CorruptedSaveError(f'Missing {line_num} line in the file')

    try:
        return data_type(data[column])
    except ValueError:
        raise CorruptedSaveError(
            f'Data in {column} column in {line_num} line is incorrect!')
    except IndexError:
        raise CorruptedSaveError(
            f'Missing {column} column in {line_num} line in the file')


class Reader:

    def __init__(self, stream):
        self.save = json.loads(stream)


class ImageReader(Reader):

    def read(self):
        return SimImage(size=self._get_size(),
                        scale=self._get_scale())

    def _get_size(self):
        return self.save["image"]["size"]

    def _get_scale(self):
        return self.save["image"]["scale"]


class SimulationReader(Reader):

    def read_steps(self):
        return self.save["steps"]

    def read_time_per_step(self):
        return self.save["time_per_step"]


class CentralObjectReader(Reader):

    def read(self):
        return CentralObject(mass=self._get_mass(),
                             radius=self._get_radius(),
                             position=self._get_position())

    def _get_mass(self):
        return self.save["central_object"]["mass"]

    def _get_radius(self):
        return self.save["central_object"]["radius"]

    def _get_position(self):
        return PositionReader(self.save).read()


class PositionReader(Reader):

    def __init__(self, stream, number=None):
        super().__init__(stream)
        self.number = number

    def read(self):
        return Position(x=self._get_x(),
                        y=self._get_y())

    def _get_x(self):
        if self.number is None:
            return self.save["central_object"]["position"]["x"]
        return self.save["point_object"][self.number]["position"]["x"]

    def _get_y(self):
        if self.number is None:
            return self.save["central_object"]["position"]["y"]
        return self.save["point_object"][self.number]["position"]["y"]


class PointObjectsReader(Reader):

    def __init__(self, stream, number):
        super().__init__(stream)
        self.number = number

    def read(self):
        return PointObject(position=self._get_position(),
                           velocity=self._get_velocity())

    def _get_position(self):
        return PositionReader(self.save, self.number).read()

    def _get_velocity(self):
        return VelocityReader(self.save, self.number).read()


class VelocityReader(Reader):

    def __init__(self, stream, number):
        super().__init__(stream)
        self.number = number

    def read(self):
        return Position(x=self._get_x(),
                        y=self._get_y())

    def _get_x(self):
        return self.save["point_object"][self.number]["velocity"]["x"]

    def _get_y(self):
        return self.save["point_object"][self.number]["velocity"]["y"]


class CorruptedSaveError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
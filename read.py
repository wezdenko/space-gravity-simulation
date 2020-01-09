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

    def read(self):
        return Position(x=self._get_x(),
                        y=self._get_y())

    def _get_x(self):
        return self.save["central_object"]["position"]["x"]

    def _get_y(self):
        return self.save["central_object"]["position"]["y"]


class PointObjectsReader:

    def __init__(self, file, line):
        self._file = file
        self._line = line

    def read_position(self):
        x = read(self._file, self._line, 0, float)
        y = read(self._file, self._line, 1, float)
        return Position(x, y)

    def read_velocity(self):
        x = read(self._file, self._line, 2, float)
        y = read(self._file, self._line, 3, float)
        try:
            return Velocity(x, y)
        except FasterThanLightError as e:
            e.point_object = self._line
            raise


class CorruptedSaveError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
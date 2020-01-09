from PIL import Image
from objects import PointObject, CentralObject, TooSmallRadiusError
from physic_vectors import Velocity, Position, FasterThanLightError
white = (255, 255, 255)


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


class SimulationReader():

    def __init__(self, file):
        self._file = file

    def read_size(self):
        return read(self._file, 0, 0)

    def read_scale(self):
        return read(self._file, 0, 1, float)

    def read_steps(self):
        return read(self._file, 0, 2)

    def read_time_per_step(self):
        return read(self._file, 0, 3, float)


class CentralObjectReader:

    def __init__(self, file):
        self._file = file

    def read_mass(self):
        return read(self._file, 1, 0, float)

    def read_radius(self):
        return read(self._file, 1, 1, float)

    def read_position(self):
        x = read(self._file, 1, 2, float)
        y = read(self._file, 1, 3, float)
        return Position(x, y)


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
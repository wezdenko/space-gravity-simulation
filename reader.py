import json
from check_errors import check_steps_error, check_time_error
from sim_image import SimImage
from objects import PointObject, CentralObject, TooSmallRadiusError
from physic_vectors import Velocity, Position, FasterThanLightError

white = (255, 255, 255)


class Reader:

    def __init__(self, stream):
        self.save = json.loads(stream)


class ImageReader(Reader):

    def read(self):
        try:
            return SimImage(size=self._get_size(),
                            scale=self._get_scale())
        except ValueError as e:
            raise CorruptedSaveError(e)
        except TypeError as e:
            raise CorruptedSaveError(e)

    def _get_size(self):
        return self.save["image"]["size"]

    def _get_scale(self):
        return self.save["image"]["scale"]


class SimulationReader(Reader):

    def read_steps(self):
        steps = self.save["steps"]
        try:
            check_steps_error(steps)
        except ValueError as e:
            raise CorruptedSaveError(e)
        except TypeError as e:
            raise CorruptedSaveError(e)
        return steps

    def read_time(self):
        time = self.save["time_per_step"]
        try:
            check_time_error(time)
        except ValueError as e:
            raise CorruptedSaveError(e)
        except TypeError as e:
            raise CorruptedSaveError(e)
        return self.save["time_per_step"]


class CentralObjectReader(Reader):

    def read(self):
        try:
            try:
                return CentralObject(mass=self._get_mass(),
                                     radius=self._get_radius(),
                                     position=self._get_position())
            except TypeError as e:
                raise CorruptedSaveError(e)
            except ValueError as e:
                raise CorruptedSaveError(e)
            except TooSmallRadiusError as e:
                raise CorruptedSaveError(e)
        except CorruptedSaveError as e:
            e.object_type = 'central object'
            raise

    def _get_mass(self):
        return self.save["central_object"]["mass"]

    def _get_radius(self):
        return self.save["central_object"]["radius"]

    def _get_position(self):
        return PositionReader(self.save).read()


class PointObjectsListReader(Reader):

    def read(self):
        point_objects_list = []
        for i in range(self.objects_number()):
            try:
                point_objects_list.append(
                    PointObjectReader(self.save, i).read())
            except CorruptedSaveError as e:
                e.object_num = i
                raise
        return point_objects_list

    def objects_number(self):
        return len(self.save["point_objects_list"])


class PointObjectReader():

    def __init__(self, dictionary, number):
        self.save = dictionary
        self.number = number

    def read(self):
        try:
            return PointObject(position=self._get_position(),
                               velocity=self._get_velocity())
        except CorruptedSaveError as e:
            e.object_type = 'point object'
            raise

    def _get_position(self):
        return PositionReader(self.save, self.number).read()

    def _get_velocity(self):
        return VelocityReader(self.save, self.number).read()


class PositionReader():

    def __init__(self, dictionary, number=None):
        self.save = dictionary
        self.number = number

    def read(self):
        try:
            return Position(x=self._get_x(),
                            y=self._get_y())
        except TypeError as e:
            raise CorruptedSaveError(e)

    def _get_x(self):
        if self.number is None:
            return self.save["central_object"]["position"]["x"]
        return self.save[
            "point_objects_list"][self.number]["point_object"]["position"]["x"]

    def _get_y(self):
        if self.number is None:
            return self.save["central_object"]["position"]["y"]
        return self.save[
            "point_objects_list"][self.number]["point_object"]["position"]["y"]


class VelocityReader():

    def __init__(self, dictionary, number):
        self.save = dictionary
        self.number = number

    def read(self):
        try:
            return Velocity(x=self._get_x(),
                            y=self._get_y())
        except TypeError as e:
            raise CorruptedSaveError(e)
        except FasterThanLightError as e:
            raise CorruptedSaveError(e)

    def _get_x(self):
        return self.save[
            "point_objects_list"][self.number]["point_object"]["velocity"]["x"]

    def _get_y(self):
        return self.save[
            "point_objects_list"][self.number]["point_object"]["velocity"]["y"]


class CorruptedSaveError(Exception):
    def __init__(self, msg, object_type=None, object_num=None):
        super().__init__(msg)
        self.object_type = object_type
        self.object_num = object_num

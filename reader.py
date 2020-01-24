import json
from sim_image import SimImage
from objects import PointObject, CentralObject, TooSmallRadiusError
from physic_vectors import Velocity, Position, FasterThanLightError
from physic_units import Steps, Time, Radius, Mass, Size, Scale


class Reader:
    '''
    Class which stores data as a dictionary
    -stream - json type dictionary
    '''

    def __init__(self, stream):
        self.save = json.loads(stream)


class ImageReader(Reader):
    '''Reads size and scale from save'''

    def read(self):
        '''returns SimImage object'''
        try:
            return SimImage(size=Size(self._get_size()),
                            scale=Scale(self._get_scale()))
        except ValueError as e:
            raise CorruptedSaveError(e)
        except TypeError as e:
            raise CorruptedSaveError(e)

    def _get_size(self):
        return self.save["image"]["size"]

    def _get_scale(self):
        return self.save["image"]["scale"]


class SimulationReader(Reader):
    '''Reads steps and time per step from save'''

    def read_steps(self):
        '''returns steps (int)'''
        try:
            return Steps(self.save["steps"])
        except ValueError as e:
            raise CorruptedSaveError(e)
        except TypeError as e:
            raise CorruptedSaveError(e)

    def read_time(self):
        '''returns time per step'''
        try:
            return Time(self.save["time_per_step"])
        except ValueError as e:
            raise CorruptedSaveError(e)
        except TypeError as e:
            raise CorruptedSaveError(e)


class CentralObjectReader(Reader):
    '''Reads all central object attributes from save'''

    def read(self):
        '''returns central object'''
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
        return Mass(self.save["central_object"]["mass"])

    def _get_radius(self):
        return Radius(self.save["central_object"]["radius"])

    def _get_position(self):
        return PositionReader(self.save).read()


class PointObjectsListReader(Reader):
    '''Reads the list of point objects from save'''

    def read(self):
        '''returns the list of point objects'''
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
        '''returns number of point objects in save'''
        return len(self.save["point_objects_list"])


class PointObjectReader():
    '''Reads all point object attributes'''

    def __init__(self, dictionary, number):
        self.save = dictionary
        self.number = number

    def read(self):
        '''returns point object'''
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
    '''
    Reads position from given object
    -number = None - position of central object
    -number = 0 - position of first point object
    -etc...
    '''

    def __init__(self, dictionary, number=None):
        self.save = dictionary
        self.number = number

    def read(self):
        '''returns position vector object'''
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
    '''Reads velocity of given point object'''

    def __init__(self, dictionary, number):
        self.save = dictionary
        self.number = number

    def read(self):
        '''returns velocity vector object'''
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

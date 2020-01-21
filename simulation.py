import reader
import writer
import json
from console_input import (image_input, steps_input, time_input,
                           central_object_input, point_objects_list_input)


black = (0, 0, 0)
grey = (150, 150, 150)
white = (255, 255, 255)


class Simulation:
    '''
    This class represents whole simulation and contains all varriables.
    Attributes cannot be set while initiating the simulation object, use
    special methods for it (load_from_file() or data_input()).
    '''

    def __init__(self):
        self._image = None
        self.steps = None
        self.time_per_step = None
        self.central_object = None
        self.point_objects = []

    '''Property Decorators'''

    @property
    def size(self):
        return self._image.size

    @property
    def scale(self):
        return self._image.scale

    '''Methods'''

    def load_from_file(self, file_path):
        '''takes path to a json file and loads all attributes from the file
        (do not give extension in file name)'''
        with open(f'{file_path}.json') as file:
            stream = file.read()
            self._load_attributes(stream)

    def _load_attributes(self, stream):
        '''takes stream of strings from file (e.g. file.read()) and loads
        attributes using reader.py classes'''
        self._image = reader.ImageReader(stream).read()
        self.steps = reader.SimulationReader(stream).read_steps()
        self.time_per_step = reader.SimulationReader(stream).read_time()
        self.central_object = reader.CentralObjectReader(stream).read()
        self.point_objects = reader.PointObjectsListReader(stream).read()

    def save_to_file(self, file_path):
        '''Saves data from the simulation to json file (do not give extension
        in file name)'''
        with open(f'{file_path}.json', 'w') as file:
            file.write(self._prepare_save())

    def _prepare_save(self):
        '''Takes data from all attributes and using writer.py classes returns
        json formated data'''
        save = {}
        save.update(writer.ImageWriter(self._image).write())
        save.update(writer.StepsWriter(self.steps).write())
        save.update(writer.TimeWriter(self.time_per_step).write())
        save.update(writer.CentralObjectWriter(self.central_object).write())
        save.update(writer.PointObjectsListWriter(self.point_objects).write())
        return json.dumps(save)

    def data_input(self):
        '''This method lets user loads all data from console'''
        self._attributes_values_input()

    def _attributes_values_input(self):
        '''Loads all attributes using console_input.py classes'''
        self._image = image_input()
        self.steps = steps_input()
        self.time_per_step = time_input()
        self.central_object = central_object_input()
        self.point_objects = point_objects_list_input()

    def draw_pixel(self, x, y, color):
        '''changes color of the chosen pixel
        -x - horizontal pixel value
        -y - vertical pixel value
        -color - RGB tuple (from 0 to 255)'''
        try:
            if x < 0 or y < 0:
                raise IndexError
            self._image.pixels()[x, y] = color
        except IndexError:
            pass

    def draw_point_objects(self, color):
        '''Change color of the pixels which all point objects are located
        on.'''
        for point_object in self.point_objects:
            x, y = point_object.check_pixel(self.scale)
            self.draw_pixel(x, y, color)

    def draw_radius(self):
        '''call this function to draw the radius of central object'''
        x, y = self.central_object.check_pixel(self.scale)
        radius = self.central_object.pixel_radius(self.scale)

        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if self.central_object.is_inside_radius((i, j), self.scale):
                    self.draw_pixel(i, j, (31, 78, 89))
        self.draw_pixel(x, y, (200, 30, 30))

    def is_on_same_pixel(self, first_obj, second_obj):
        '''Bool function - checks if two objects are located on the same
        pixel'''
        return first_obj.is_on_same_pixel(second_obj, self.scale)

    def collide_with_central_object(self, point_obj):
        '''Remove all point objects from list which collided with central
        object (use not recommended)'''
        x, y = point_obj.check_pixel(self.scale)
        if self.central_object.is_inside_radius((x, y), self.scale):
            self.point_objects.remove(point_obj)

    def collide_point_objects(self, first_obj, second_obj):
        '''Checks if two point objects are on the same pixels and if true,
        removes both of them from the list (use not recommended)'''
        if self.is_on_same_pixel(first_obj, second_obj):
            self.point_objects.remove(first_obj)
            self.point_objects.remove(second_obj)

    def update_all_colisions(self):
        '''Checks if any collisions in particular time occured and if so,
        removes these objects. (that's the function you want to use)'''
        for i, first_obj in enumerate(self.point_objects):
            for second_obj in self.point_objects[i+1:]:
                self.collide_point_objects(first_obj, second_obj)
            self.collide_with_central_object(first_obj)

    def save_image(self, file_name):
        '''Saves the image of the simulation as a png file. (do not give
        extension in file name)'''
        self._image.save(file_name)

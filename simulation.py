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
        self._steps = None
        self._time_per_step = None
        self.central_object = None
        self._point_objects = []

    '''Property Decorators'''

    @property
    def size(self):
        return self._image.size

    @property
    def scale(self):
        return self._image.scale

    @property
    def steps(self):
        return self._steps

    @property
    def time_per_step(self):
        return self._time_per_step

    '''Methods'''

    def load_from_file(self, file_path):
        '''takes path to a file and loads all attributes from the file
        (no more input is needed)'''
        with open(f'{file_path}.json') as file:
            stream = file.read()
            self._load_attributes(stream)

    def _load_attributes(self, stream):
        self._image = reader.ImageReader(stream).read()
        self._steps = reader.SimulationReader(stream).read_steps()
        self._time_per_step = reader.SimulationReader(stream).read_time()
        self.central_object = reader.CentralObjectReader(stream).read()
        self._point_objects = reader.PointObjectsListReader(stream).read()

    def save_to_file(self, file_path):
        with open(f'{file_path}.json', 'w') as file:
            file.write(self._prepare_save())

    def _prepare_save(self):
        save = {}
        save.update(writer.ImageWriter(self._image).write())
        save.update(writer.StepsWriter(self.steps).write())
        save.update(writer.TimeWriter(self.time_per_step).write())
        save.update(writer.CentralObjectWriter(self.central_object).write())
        save.update(writer.PointObjectsListWriter(self._point_objects).write())
        return json.dumps(save)

    def data_input(self):
        self._attributes_values_input()

    def _attributes_values_input(self):
        self._image = image_input()
        self._steps = steps_input()
        self._time_per_step = time_input()
        self.central_object = central_object_input()
        self._point_objects = point_objects_list_input()

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
        for point_object in self._point_objects:
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
        return first_obj.is_on_same_pixel(second_obj, self.scale)

    def collide_with_central_object(self, point_obj):
        x, y = point_obj.check_pixel(self.scale)
        if self.central_object.is_inside_radius((x, y), self.scale):
            self._point_objects.remove(point_obj)

    def collide_point_objects(self, first_obj, second_obj):
        if self.is_on_same_pixel(first_obj, second_obj):
            self._point_objects.remove(first_obj)
            self._point_objects.remove(second_obj)

    def update_all_colisions(self):
        for i, first_obj in enumerate(self._point_objects):
            for second_obj in self._point_objects[i+1:]:
                self.collide_point_objects(first_obj, second_obj)
            self.collide_with_central_object(first_obj)

    def save(self, file_name):
        self._image.save(file_name)


if __name__ == "__main__":
    sim = Simulation()
    print(writer.__doc__)

from PIL import Image
from sim_image import SimImage
from objects import PointObject, CentralObject, TooSmallRadiusError
import reader

black = (0, 0, 0)
grey = (150, 150, 150)
white = (255, 255, 255)


def read(lines, line_num, argument=None):
    data = lines[line_num].strip().split(',')
    if argument is None:
        return data
    return int(data[argument])


def value_input(message):
    try:
        value = int(input(f'{message}: '))
        if value < 1:
            raise ValueError
        else:
            return value
    except ValueError:
        print(f'{message} must be an intiger greater than 1!')
        return value_input(message)


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

    '''Setters'''

    @steps.setter
    def steps(self, value):
        if type(value) != int:
            raise TypeError(f'Steps must be an intiger: {value}')
        elif value <= 0:
            raise ValueError(f'Steps must be positive: {value}')
        self._steps = value

    @time_per_step.setter
    def time_per_step(self, value):
        if type(value) != float and type(value) != int:
            raise TypeError(f'Time must be float or intiger: {value}')
        elif value <= 0:
            raise ValueError(f'Time must be positive: {value}')
        self._time_per_step = value

    '''Methods'''

    def load_from_file(self, file_path):
        '''takes path to a file and loads all attributes from the file
        (no more input is needed)'''
        with open(file_path) as file:
            stream = file.read()
            self._image = reader.ImageReader(stream).read()
            self._steps = reader.SimulationReader(stream).read_steps()
            self._time_per_step = reader.SimulationReader(stream).read_time()
            self.central_object = reader.CentralObjectReader(stream).read()
            self._point_objects = reader.PointObjectsListReader(stream).read()

    def data_input(self):
        self._simulation_values_input()

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

    '''private methods for data_input'''

    def _simulation_values_input(self):
        size = value_input('Size')
        self.image = Image.new('RGB', (size, size), white)
        self.scale = value_input('Scale')
        self.steps = value_input('Steps')
        self.time_per_step = value_input('Time per step')

    def _set_point_objects_values(self):
        point_objects_list = []
        num_of_objects = value_input('Number of point objects: ')
        for i in range(num_of_objects):
            point_objects_list.append(
                PointObject(position_vector_input(self.image.size, self.scale),
                            velocity_vector_input()))
        return point_objects_list


class SizeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


if __name__ == "__main__":
    sim = Simulation()
    sim.load_from_file('saves/save1.json')
    print('yupi')

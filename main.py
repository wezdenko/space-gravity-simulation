from simulation import Simulation
from reader import CorruptedSaveError
from json import decoder
from console_input import InputError

black = (0, 0, 0)
grey = (150, 150, 150)
white = (255, 255, 255)


class OutsideImageError(Exception):
    pass


'''
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


def simulation_values_input():
    size = value_input('Size')
    scale = value_input('Scale')
    steps = value_input('Steps')
    seconds = value_input('Time per step')

    return (size, scale, steps, seconds)


def set_point_objects_values(num_of_objects, img_size, img_scale):
    point_obejcts_list = []
    for i in range(num_of_objects):
        point_obejcts_list.append(
            PointObject(position_vector_input(img_size, img_scale),
                        velocity_vector_input()))
    return point_obejcts_list


def set_central_object_values(img_size, img_scale):
    try:
        central_object = CentralObject(
            value_input('Mass'),
            value_input('Radius'),
            position_vector_input(img_size, img_scale))
        return central_object
    except TooSmallRadiusError:
        print('Radius is too small compared to mass!')
        return set_central_object_values(img_size, img_scale)


def velocity_vector_input():
    print('Give values of velocity vector')
    try:
        x_value = float(input('x_value: '))
        y_value = float(input('y_value: '))
        return Velocity(x_value, y_value)
    except ValueError:
        print('Value must be a float!')
        return velocity_vector_input()
    except FasterThanLightError:
        print('Velocity of an object cannot be faster than speed of light!')
        return velocity_vector_input()


def position_vector_input(img_size, img_scale):
    print('Give values of position vector')
    try:
        x_value = float(input('x_value: '))
        y_value = float(input('y_value: '))
        point_object = PointObject(Position(x_value, y_value))

        if point_object.check_if_inside_img(img_size, img_scale):
            return Position(x_value, y_value)
        else:
            raise OutsideImageError()

    except ValueError as e:
        print('Value must be a float or int!', e)
        return position_vector_input(img_size, img_scale)
    except OutsideImageError():
        print('Position is outside the image!')
        return position_vector_input(img_size, img_scale)
'''


def is_yes(input_value):
    if input_value.lower() == 'yes':
        return True
    elif input_value.lower() == 'no':
        return False
    else:
        raise InputError(f'"{input_value}" isn\'t "yes" or "no"')


def make_simulation_save(simulation):
    print('Do you want to save the simulation? (Yes/No)')
    try:
        if is_yes(input()):
            simulation.save_to_file('saves/new_save')
    except InputError as e:
        print('Incorrect input, type "yes" or "no".', e, end='\n\n')
        make_simulation_save(simulation)


def choose_input(simulation):
    print('Do you want to load simulation from save? (Yes/No)')
    try:
        if is_yes(input()):
            load_from_file(simulation)
        else:
            load_from_console(simulation)
    except InputError as e:
        print('Incorrect input, type "yes" or "no".', e, end='\n\n')
        choose_input(simulation)


def load_from_file(simulation):
    try:
        simulation.load_from_file('saves/save2')
    except decoder.JSONDecodeError:
        print('File cannot be read! (incorrect syntax)')
        choose_input(simulation)
    except KeyError as e:
        print(f'File cannot be read! Couldn\'t find key: {e}')
        choose_input(simulation)
    except CorruptedSaveError as e:
        if e.object_type is not None:
            if e.object_num is not None:
                print('File contains incorrect data!')
                print(f'In {e.object_type} no. {e.object_num}:', e)
            else:
                print('File contains incorrect data!')
                print(f'In {e.object_type}:', e)
        else:
            print('File contains incorrect data!', e)
        choose_input(simulation)


def load_from_console(simulation):
    simulation.data_input()


def main():
    sim = Simulation()

    choose_input(sim)

    sim.draw_radius()

    for i in range(sim.steps):
        sim.update_all_colisions()
        for point_object in sim._point_objects:
            x, y = point_object.check_pixel(sim.scale)
            sim.draw_pixel(x, y, grey)

            point_object.update_velocity(sim.central_object, sim.time_per_step)
            point_object.update_position(sim.time_per_step)

            x, y = point_object.check_pixel(sim.scale)
            sim.draw_pixel(x, y, black)

    sim.save('obraz')

    make_simulation_save(sim)


if __name__ == '__main__':
    main()

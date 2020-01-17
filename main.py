from simulation import Simulation
from reader import CorruptedSaveError
from json import decoder
from console_input import InputError

black = (0, 0, 0)
grey = (150, 150, 150)


def is_yes(input_value):
    if input_value.lower() == 'yes':
        return True
    elif input_value.lower() == 'no':
        return False
    else:
        raise InputError(f'"{input_value}" isn\'t "yes" or "no"')


def decide_to_save(simulation):
    print('Do you want to save the simulation? (Yes/No)')
    try:
        if is_yes(input()):
            make_simulation_save(simulation)
    except InputError as e:
        print('Incorrect input, type "yes" or "no".', e)
        decide_to_save(simulation)


def make_simulation_save(simulation):
    try:
        simulation.save_to_file(input('Enter file name: '))
    except FileNotFoundError:
        print('Directory not found!')
        make_simulation_save(simulation)
    except OSError:
        print('Couldn\'t save the file! Incorrect file name!')
        make_simulation_save(simulation)


def make_image_save(simulation):
    try:
        simulation.save_image(input('Enter name of the image: '))
    except FileNotFoundError:
        print('Directory not found!')
        make_image_save(simulation)
    except OSError:
        print('Couldn\'t save the file! Incorrect file name!')
        make_image_save(simulation)


def choose_input(simulation):
    print('Do you want to load simulation from save? (Yes/No)')
    try:
        if is_yes(input()):
            load_from_file(simulation)
        else:
            simulation.data_input()
    except InputError as e:
        print('Incorrect input, type "yes" or "no".', e, end='\n\n')
        choose_input(simulation)


def load_from_file(simulation):
    try:
        simulation.load_from_file(input('Enter file name: '))
    except FileNotFoundError:
        print('File not found!')
        load_from_file(simulation)
    except OSError:
        print('Incorrect file name, enter other name!')
        load_from_file(simulation)
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

    make_image_save(sim)

    decide_to_save(sim)


if __name__ == '__main__':
    main()

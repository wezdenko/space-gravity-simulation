from simulation import Simulation
from reader import CorruptedSaveError
from json import decoder
from console_input import InputError

# colors for pixels
black = (0, 0, 0)
grey = (150, 150, 150)
bluish = (31, 78, 89)


def is_yes(input_value):
    '''Bool function - checks if input form console is "yes" or "no" or
    neither.'''
    if input_value.lower() == 'yes':
        return True
    elif input_value.lower() == 'no':
        return False
    else:
        raise InputError(f'"{input_value}" isn\'t "yes" or "no"')


def decide_to_save(simulation):
    '''This function lets user decide if he wants to save the simulation
    in json file.'''
    print('Do you want to save the simulation? (Yes/No)')
    try:
        if is_yes(input()):
            make_simulation_save(simulation)
    except InputError as e:
        print('Incorrect input, type "yes" or "no".', e)
        decide_to_save(simulation)


def make_simulation_save(simulation):
    '''Takes file name from console, checks if it's correct and pass this
    name to "save to file method".'''
    try:
        simulation.save_to_file(input('Enter file name: '))
    except FileNotFoundError:
        print('Directory not found!')
        make_simulation_save(simulation)
    except OSError:
        print('Couldn\'t save the file! Incorrect file name!')
        make_simulation_save(simulation)


def make_image_save(simulation):
    '''Takes image name from console, checks if it's correct and pass it
    to "save image method".'''
    try:
        simulation.save_image(input('Enter name of the image: '))
    except FileNotFoundError:
        print('Directory not found!')
        make_image_save(simulation)
    except OSError:
        print('Couldn\'t save the file! Incorrect file name!')
        make_image_save(simulation)


def choose_input(simulation):
    '''This function lets user decide if data is taken from json file
    or from console.'''
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
    '''Takes json file name and calls "load form file" method, also checks if
    file has corrcect syntax and values.'''
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
    '''Calls all methods and fucntions and runs whole program.'''

    # creates simulation object
    sim = Simulation()

    # chooses if data for simulation is passed from file or console
    # and then loads this data to simulation object
    choose_input(sim)

    # draw radius of the central object given colour
    sim.draw_radius(bluish)

    # loop which updates simulation "steps" times
    for i in range(sim.steps):

        # checks if any collisions between objects happend and updates them
        sim.update_all_colisions()

        # this loop iterates through all point objects
        for point_object in sim.point_objects:

            # these two lines draw point object trail
            x, y = point_object.check_pixel(sim.scale)
            sim.draw_pixel(x, y, grey)

            # calculates point object velocity in gravitational field
            point_object.update_velocity(sim.central_object, sim.time_per_step)
            # calculates point object position after "time_per_step" time
            point_object.update_position(sim.time_per_step)

            # these two lines draw point object current position
            x, y = point_object.check_pixel(sim.scale)
            sim.draw_pixel(x, y, black)

    # saves image of the simulation
    make_image_save(sim)

    # chooses if values of the simulation are saves in json fle
    decide_to_save(sim)


if __name__ == '__main__':
    main()

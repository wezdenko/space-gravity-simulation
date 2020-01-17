def create_file(file_path):
    try:
        with open(f'{file_path}.txt', 'w') as file:
            file.write('created')
    except FileNotFoundError as e:
        print(e)
    except OSError as e:
        print(e)

create_file(input())
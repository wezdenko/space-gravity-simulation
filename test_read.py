'''
def read(lines, line_num, argument=None):
    data = lines[line_num].strip().split(',')
    if argument is None:
        return data
    return int(data[argument])
'''

def read(lines):
    return lines.readlines()


def test_read():
    with open('saves/save1.txt', 'r') as f:
        print(read(f))
        print(read(f))

test_read()
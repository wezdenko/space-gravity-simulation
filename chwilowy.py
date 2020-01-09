lista = ['a', 'b']

for i, letter in enumerate(lista):
    for letter2 in lista[i+1:]:
        print(f'{letter} = {letter2}')
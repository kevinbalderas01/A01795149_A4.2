'''
sys -> To get parameters from terminal
os -> To manage files, creation and deletion
time -> To manage start and end time to measure execution
'''

# pylint: disable=invalid-name
import sys
import os
import time

def read_file(filename):
    '''
    Función encargada de leer el archivo para calcular estadisticas
    '''
    lst = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            lst.append(line.strip())
    return lst

def count_words(words):
    '''
    Esta función hace el conteo de frecuencia de cada palabra
    '''
    new_dict = {}
    for word in words:
        try:
            new_dict[word] = new_dict[word] + 1
        except KeyError:
            new_dict[word] = 1
    return new_dict



def write_info_file(data, final_time, start_time):
    '''
    La función escriba la información en el archivo de salida correspondiente
    '''
    with open('WordCountResults.txt', 'w', encoding='utf-8') as file:
        file.write('Row labels , WordCount\n')
        ordered_dict = dict(sorted(data.items(), key=lambda z: z[1], reverse=True))
        for key, value in ordered_dict.items():
            file.write(f'{key}\t{value}\n')
        file.write(f'Grand total, {sum(list(ordered_dict.values()))}\n')
        file.write(f'Tiempo de execucion en segundos: {final_time-start_time}')


def delete_final_file(path='WordCountResults.txt'):
    '''
    Esta función elimina el archivo final en caso de existir para sobrescribirlo con cada ejecución
    '''
    if os.path.isfile(path):
        os.remove(path)

def main():
    '''
    Ejecución principal del programa
    '''
    delete_final_file()
    start_time = time.time()
    print('Inicio de programa')
    try:
        path = sys.argv[1]
        words = read_file(path)
        new_dict = count_words(words)
        final_time = time.time()
        write_info_file(new_dict, final_time, start_time)
        print('Fin de execución')
    except FileNotFoundError:
        print('No se encontró archivo. Debes ingresar un archivo para calcular estadísticas')

if __name__=='__main__':
    main()
        
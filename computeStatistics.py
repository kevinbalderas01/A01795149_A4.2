'''
sys -> To get parameters from terminal
os -> To manage files, creation and deletion
time -> To manage start and end time to measure execution
'''
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

def get_mean(lst):
    '''
    Esta función calcula el promedio de un fonjunto de datos
    '''
    return sum(lst)/len(lst)

def get_variance(lst, mean):
    '''
    Esta función calcula la varianza del conjunto de datos
    '''
    n = len(lst)
    item_minus_mean = [(element - mean)**2 for element in lst]
    return sum(item_minus_mean)/(n-1)

def get_std(variance):
    '''
    Esta función calcula la desviación estandar del conjunto de datos
    '''
    return variance**0.5

def get_median(lst):
    '''
    Esta función calcula la mediana del conjunto de datos
    '''
    lst = sorted(lst)
    n =len(lst)
    if n%2 == 0:
        med = (lst[-1+(n//2)] + lst[-1+(1+(n//2))] ) / 2
    else:
        med = lst[-1+((n+1)//2)]
    return med

def get_mode(lst):
    '''
    Esta función calcula la moda de un conjunto de datos
    '''
    dct_freq = {}
    for element in lst:
        dct_freq[element] = 0
    for element in lst:
        dct_freq[element] = dct_freq[element]+1
    return max(dct_freq.items(), key=lambda x: x[1])

def manage_list(lst):
    new_list = []
    for element in lst:
        try:
            i = float(element)
            new_list.append(i)
        except:
            continue
    return new_list

def calc_statistics(lst):
    '''
    Esta función hace el cálculo de todos los estadisticos requeridos
    '''
    lst = manage_list(lst)
    mean = get_mean(lst)
    variance = get_variance(lst, mean)
    std = get_std(variance)
    median = get_median(lst)
    mode = get_mode(lst)
    print(f'Mean: {mean}')
    print(f'Median: {median}')
    print(f'Moda: {mode[0]}')
    print(f'Variance: {variance}')
    print(f'Standard Deviation: {std}')
    return (mean, variance, std, median, mode)

def write_info_file(data):
    '''
    La función escriba la información en el archivo de salida correspondiente
    '''
    mean, variance , std , median, mode, start_time, final_time = data
    with open('StatisticsResults.txt', 'w', encoding='utf-8') as file:
        file.write(f'Mean: {mean}\n')
        file.write(f'Median: {median}\n')
        file.write(f'Moda: {mode[0]}\n')
        file.write(f'Variance: {variance}\n')
        file.write(f'Standard Deviation: {std}\n')
        file.write(f'Tiempo de execucion en segundos: {final_time-start_time}')


def delete_final_file(path='StatisticsResults.txt'):
    '''
    Esta función elimina el archivo final en caso de existir para sobrescribirlo con cada ejecución
    '''
    if os.path.isfile(path):
        os.remove(path)

def main():
    '''
    Ejecución principal del programa
    '''
    start_time = time.time()
    print('Inicio de programa')
    try:
        path = sys.argv[1]
        numbers = read_file(path)
        mean, variance , std , median, mode = calc_statistics(numbers)
        final_time = time.time()
        print(f'Tiempo de execucion en segundos: {final_time-start_time}')
        delete_final_file()
        write_info_file((mean, variance , std , median, mode, start_time, final_time))
        print('Fin de execución')
    except IndexError:
        print('No se encontró archivo. Debes ingresar un archivo para calcular estadísticas')

if __name__=='__main__':
    main()
        
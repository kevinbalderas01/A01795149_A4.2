'''
sys -> To get parameters from terminal
os -> To manage files, creation and deletion
time -> To manage start and end time to measure execution
'''

# pylint: disable=invalid-name
import sys
import os
import time

hex_dict = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8',
            '9':'9','10':'A','11':'B','12':'C','13':'D','14':'E','15':'F'}
dict_hex_inv={y: x for x, y in hex_dict.items()}

def read_file(filename):
    '''
    Función encargada de leer el archivo para calcular estadisticas
    '''
    lst = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            lst.append(line.strip())
    return lst

def manage_list(lst):
    '''
    Esta función convierte la lista de contenido de archivos en numeros y 
    elimina tipos de datos que no son números
    '''
    new_list = []
    for element in lst:
        try:
            i = int(element)
            new_list.append(i)
        except ValueError:
            continue
    return new_list

def make_conversion(number):
    '''
    Conversión de un número decimal a binario
    '''
    if number == 0:
        return '0'
    lst = []
    while number / 2  > 0:
        lst.insert(0,str(number % 2))
        number = number //2
    return ''.join(lst)

def refill_bits(string):
    '''
    Esta función hace de auxiliar para el complemento a dos en caso de números negativos
    Rellena con 0 hasta cumplir con 8 bits
    '''
    n_bits = 8
    n_number = len(string)
    return (('0'*(n_bits-n_number)) + string)

def find_first_one(string):
    '''
    Este método auxilia en el complemento a dos
    Encuentra el primero uno para que apartir de ahí se haga el inverso de los demás numeros
    '''
    #We look for the first 1 to make the change, according to 'TWO COMPLEMENT'
    n = len(string)
    for i in range(n-1, 0, -1):
        if string[i]=='1':
            idx = i
            break
    return idx

def change_values(string, idx):
    '''
    Esta función cambia el valor de los bits binarios para el complemento a dos
    '''
    new_value = []
    for i,_ in enumerate(string[:idx]):
        if string[i] == '0':
            new_value.append('1')
        else:
            new_value.append('0')
    for j in range(idx, len(string)):
        new_value.append(string[j])
    return ''.join(new_value)

def convert_to_binary(numbers):
    '''
    Esta función decide que hacer con números binarios sean positivos o negativos
    '''
    lst = []
    for number in numbers:
        if number >=0:
            binary_str = make_conversion(number)
            lst.append(binary_str)
        #Negative number, We apply 'complement Two' technique
        else:
            number_str = str(number)
            binary_no_sign = make_conversion(int(number_str[1:]))
            binary_no_sign = refill_bits(binary_no_sign)
            idx_first_one = find_first_one(binary_no_sign)
            number_converted = change_values(binary_no_sign, idx_first_one)
            lst.append(number_converted)
    return lst

def get_conversion_hex(number_decimal):
    '''
    Función que hace un mapeado de numeros decimales a hexadecimales
    '''
    try:
        return hex_dict[number_decimal]
    except ValueError:
        return 0

def make_conversion_hex(number):
    '''
    Esta función hace la división normal entre 16 para pasar de decimal 
    positivo a hexadecimal positivo
    '''
    if number == 0:
        return '0'
    lst = []
    while number / 16  > 0:
        lst.insert(0,get_conversion_hex(str(number % 16)))
        number = number //16
    return ''.join(lst)

def manage_neg_hex(hex_str):
    '''
    Esta función transforma a negativos, teniendo en cuenta el complemento a dos
    '''
    result = []
    new_val = 0
    number_converted = make_conversion_hex(int(str(hex_str)[1:]))
    num_split_str = list(str(number_converted))
    n_bits_tofill = 8-len(num_split_str)
    max_value = sorted(num_split_str)[-1]
    for i,_ in enumerate(num_split_str):
        numeric_val = dict_hex_inv[num_split_str[i]]
        if num_split_str[i] != max_value:
            new_val = 15-int(numeric_val)
        if num_split_str[i] == max_value:
            new_val = 15-int(numeric_val) + 1
        if num_split_str[i] == '0':
            new_val = 0
        result.append(get_conversion_hex(str(new_val)))
    result = ['F']*n_bits_tofill + result
    return ''.join(result)

def convert_to_hex(numbers):
    '''
    Esta función convierte de decimal a hexadecimal, tomando en cuenta si es positivo o negativo
    '''
    lst = []
    for number in numbers:
        if number >=0:
            hex_str = make_conversion_hex(number)
            lst.append(hex_str)
        else:
            #here we deal with negative numbers
            converted_negative = manage_neg_hex(number)
            lst.append(converted_negative)
    return lst

def write_info_file(data):
    '''
    La función escriba la información en el archivo de salida correspondiente
    '''
    numbers, binary, hexa, final_time, start_time = data
    with open('ConversionResults.txt', 'w', encoding='utf-8') as file:
        file.write('Numero decimal , Binario, Hexadecimal\n')
        for items in zip(numbers, binary, hexa):
            file.write(f'{items[0]}, {items[1]}, {items[2]}\n')
        file.write(f'Tiempo de execucion en segundos: {final_time-start_time}')


def delete_final_file(path='ConversionResults.txt'):
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
    delete_final_file()
    print('Inicio de programa')
    try:
        path = sys.argv[1]
        numbers = read_file(path)
        numbers = manage_list(numbers)
        numbert_to_binary = convert_to_binary(numbers)
        numbert_to_hex = convert_to_hex(numbers)
        final_time = time.time()
        write_info_file([numbers,numbert_to_binary, numbert_to_hex, final_time, start_time])
        print('Fin de execución')
    except FileNotFoundError:
        print('No se encontró archivo. Debes ingresar un archivo para calcular estadísticas')

if __name__=='__main__':
    main()
        
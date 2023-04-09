# uma função simples que tenta converter um valor para float e em seguida verifica se é positivo, o retorno será
# False caso não seja possível converter ou caso o valor seja menor que 0
def is_positive_number(value):
    try:
        number_string = float(value)
    except ValueError:
        return False
    return number_string > 0
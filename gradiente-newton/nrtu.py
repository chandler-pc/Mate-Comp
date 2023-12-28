import random

def to_base_3(decimal):
    if decimal == 0:
        return "0"
    result = ""
    while decimal > 0:
        mod = decimal % 3
        result = str(mod) + result
        decimal //= 3
    return result

def complete_to_5(array):
    while len(array) < 6:
        array.insert(0, "0")
    return array

message = list("HOLA")
ascii = [ord(c) for c in message]
base_3 = [to_base_3(c) for c in ascii]
random_value = base_3[random.randint(0, len(base_3) - 1)]
S = list(random_value)
polynom_message = complete_to_5(S)
values_polynom = ['-1','0','1']
polynom_f = [values_polynom[random.randint(0,len(values_polynom)-1)] for _ in range(len(polynom_message))]

print(polynom_f)


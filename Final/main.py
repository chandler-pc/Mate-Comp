from mip import *
from itertools import permutations

def main():
    print("Starting program...")
    try:
        model = Model()
    except Exception as e:
        print("An error occurred:", e)
    print("Model created")
    W = 0
    H = 0
    D = 0
    w = list()
    h = list()
    d = list()

    m = list()
    print("Reading file...")
    with open('input.txt') as f:
        print("File readed")
        for index, line in enumerate(f.readlines()):
            separated_values = line.replace('\n', '').split(' ')
            separated_values = [float(value) for value in separated_values]

            if index == 0:
                W = float[separated_values[0]]
                H = float[separated_values[1]]
                D = float[separated_values[2]]
            else:
                posible_permutation = set(permutations(separated_values,3))
                m.append(len(posible_permutation))

                w.append([value[0] for value in posible_permutation])
                h.append([value[1] for value in posible_permutation])   
                d.append([value[2] for value in posible_permutation])

    numberOfVariables = index

    x = list()
    y = list()
    z = list()

    s = list()
    left = list()
    right = list()
    under = list()
    over = list()
    behind = list()
    inFront = list()

    for i in range(numberOfVariables):
        x.append(model.add_var(name=f'x_{i+1}', var_type=CONTINUOUS, lb=0))
        y.append(model.add_var(name=f'y_{i+1}', var_type=CONTINUOUS, lb=0))
        z.append(model.add_var(name=f'z_{i+1}', var_type=CONTINUOUS, lb=0))

        s.append(list())
        for k in range(m[i]):
            s[i].append(model.add_var(name=f's_{i+1}_{k+1}', var_type=BINARY))

        left[i] = dict()
        right[i] = dict()
        under[i] = dict()
        over[i] = dict()
        behind[i] = dict()
        inFront[i] = dict()

        for j in range(i+1, numberOfVariables):
            left[i][j] = model.add_var(name=f'l_{i+1}_{j+1}', var_type=BINARY)
            right[i][j] = model.add_var(name=f'r_{i+1}_{j+1}', var_type=BINARY)
            under[i][j] = model.add_var(name=f'u_{i+1}_{j+1}', var_type=BINARY)
            over[i][j] = model.add_var(name=f'o_{i+1}_{j+1}', var_type=BINARY)
            behind[i][j] = model.add_var(name=f'b_{i+1}_{j+1}', var_type=BINARY)
            inFront[i][j] = model.add_var(name=f'f_{i+1}_{j+1}', var_type=BINARY)


    model.objective = maximize(xsum(s[i][k] for i in range(numberOfVariables) for k in range(m[i])))

    for i in range(numberOfVariables):
        for j in range(i+1, numberOfVariables):
            model += left[i][j] + right[i][j] + under[i][j] + over[i][j] + behind[i][j] + inFront[i][j] >= xsum(s[i][k] for k in range(m[i])) + xsum(s[j][k] for k in range(m[j])) - 1

            model += left[i][j] + right[i][j] + under[i][j] + over[i][j] + behind[i][j] + inFront[i][j] <= xsum(s[i][k] for k in range(m[i])) + xsum(s[j][k] for k in range(m[i]))
            model += left[i][j] + right[i][j] + under[i][j] + over[i][j] + behind[i][j] + inFront[i][j] <= xsum(s[i][k] for k in range(m[i])) + xsum(s[j][k] for k in range(m[j]))

            model += x[i] - x[j] + W * left[i][j] <= W - xsum(s[i][k] * w[i][k] for k in range(m[i]))
            model += x[j] - x[i] + W * right[i][j] <= W - xsum(s[j][k] * w[j][k] for k in range(m[j]))

            model += y[i] - y[j] + H * under[i][j] <= H - xsum(s[i][k] * h[i][k] for k in range(m[i]))
            model += y[j] - y[i] + H * over[i][j] <= H - xsum(s[j][k] * h[j][k] for k in range(m[j]))

            model += z[i] - z[j] + D * behind[i][j] <= D - xsum(s[i][k] * d[i][k] for k in range(m[i]))
            model += z[j] - z[i] + D * inFront[i][j] <= D - xsum(s[j][k] * d[j][k] for k in range(m[j]))

        model += xsum(s[i][k] for k in range(m[i])) == 1
    
    for i in range(numberOfVariables):
        model += x[i] <= W -xsum(s[i][k] * w[i][k] for k in range(m[i]))
        model += y[i] <= H -xsum(s[i][k] * h[i][k] for k in range(m[i]))
        model += z[i] <= D -xsum(s[i][k] * d[i][k] for k in range(m[i]))

    model.max_gap = 0.05
    status = model.optimize(max_seconds=600)

    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution cost {} found'.format(model.objective_value))
        items_orientation = list()
        for v in model.vars:
            if 's' in v.name:
                if v.x >= 0.98:
                    sep_name = v.name.split('_')
                    item_name = sep_name[1]
                    items_orientation[item_name] = list()
                    items_orientation[item_name].append(w[int(sep_name[1])-1][int(sep_name[2])-1])
                    items_orientation[item_name].append(h[int(sep_name[1])-1][int(sep_name[2])-1])
                    items_orientation[item_name].append(d[int(sep_name[1])-1][int(sep_name[2])-1])
        print("Items")
        for index,v in enumerate(model.vars):
            if v.name[0] == 'x':
                sep_name = v.name.split('_')
                print(f'\tItem {sep_name[1]}:')
                print(f'\t\tPosition: [{round(v.x)}, ',end='')
            elif v.name[0] == 'y':
                print(f'{round(v.x)}, ',end='')
            elif v.name[0] == 'z':
                print(f'{round(v.x)}]')
                print(f'\t\tOrientation: {items_orientation[f'Item {sep_name[1]}']}')
        model.write('3DPacking.lp')

main()
            
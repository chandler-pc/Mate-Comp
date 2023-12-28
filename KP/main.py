import time
import random

class KP:
    def kp(self):
        print("KP seleccionado")
        capacity = int(input("Ingrese la capacidad de la mochila: "))
        items = int(input("Ingrese la cantidad de items: "))
        generate_random = input("¿Desea generar los items de forma aleatoria? (s/n): ")
        value_weight = []
        while len(value_weight) != items:
            n = len(value_weight) + 1
            if generate_random == "s":
                v = random.randint(1, 100)
                w = random.randint(1, random.randint(1, capacity))
                value_weight.append((v, w))
                print("Item {}: Valor: {:5} | Peso: {:5}".format(n, v, w))
            else:
                v = int(input("Ingrese el valor para el item {}: ".format(n)))
                w = int(input("Ingrese el peso para el item {}: ".format(n)))
                value_weight.append((v, w))
        print("La tabla de items es:")
        print("Item | Valor | Peso")
        print("-" * 21)
        for i, (v, w) in enumerate(value_weight, start=1):
            print("{:4} | {:5} | {:4}".format(i, v, w))
        print("Usando programación dinámica")
        initial_time = time.time_ns()
        best_value = self.dynamic_programming(value_weight, capacity)
        final_time = time.time_ns()
        print("Mejor valor:", best_value)
        print("Tiempo transcurrido:", final_time - initial_time, "nanosegundos")
        print("Usando búsqueda local")
        initial_time = time.time_ns()
        best_value, best_combination = self.knapsack_local_search(value_weight,capacity)
        final_time = time.time_ns()
        print("Mejor valor:", best_value)
        print("Mejor combinación:", best_combination)
        print("Tiempo transcurrido:", final_time - initial_time, "nanosegundos")
        print("Usando greedy")
        initial_time = time.time_ns()
        best_value = self.greedy(value_weight, capacity)
        final_time = time.time_ns()
        print("Mejor valor:", best_value)
        print("Tiempo transcurrido:", final_time - initial_time, "nanosegundos")
        print("Usando fuerza bruta")
        initial_time = time.time_ns()
        best_value, best_combination = self.knapsack_bruteforce(value_weight, capacity)
        final_time = time.time_ns()
        print("Mejor valor:", best_value)
        print("Mejor combinación:", best_combination)
        print("Tiempo transcurrido:", final_time - initial_time, "nanosegundos")
    
    def knapsack_bruteforce(self,value_weight, capacity):
        num_items = len(value_weight)
        best_value = 0
        best_combination = None
        for i in range(2**num_items):
            combination = [value_weight[j] for j in range(num_items) if (i & (1 << j)) > 0]
            total_weight = sum(item[1] for item in combination)
            if total_weight <= capacity:
                total_value = sum(item[0] for item in combination)
                if total_value > best_value:
                    best_value = total_value
                    best_combination = combination
        return best_value, best_combination
    
    def knapsack_local_search(self, value_weight, capacity, max_iterations=1000):
        current_solution = self.generate_initial_solution(value_weight)
        current_value = self.evaluate_solution(current_solution, value_weight, capacity)
        for _ in range(max_iterations):
            neighbor_solution = self.generate_neighbor_solution(current_solution, len(value_weight))
            neighbor_value = self.evaluate_solution(neighbor_solution, value_weight, capacity)
            if neighbor_value > current_value:
                current_solution = neighbor_solution
                current_value = neighbor_value
        return current_value, current_solution

    def generate_initial_solution(self, value_weight):
        return [1, *[0 for _ in range(len(value_weight)-1)]]

    def generate_neighbor_solution(self, current_solution, num_elements):
        neighbor_solution = current_solution.copy()
        i = random.randint(0, num_elements-1)
        neighbor_solution[i] = 1 - neighbor_solution[i]
        return neighbor_solution

    def evaluate_solution(self, solution, value_weight, capacity):
        total_value = sum(item[0] * solution[i] for i, item in enumerate(value_weight))
        total_weight = sum(item[1] * solution[i] for i, item in enumerate(value_weight))
        if total_weight > capacity:
            return 0
        else:
            return total_value
        
    def dynamic_programming(self, value_weight, capacity):
        num_items = len(value_weight)
        table = [[0 for _ in range(capacity+1)] for _ in range(num_items+1)]
        for i in range(1, num_items+1):
            for j in range(1, capacity+1):
                v, w = value_weight[i-1]
                if w > j:
                    table[i][j] = table[i-1][j]
                else:
                    table[i][j] = max(table[i-1][j], table[i-1][j-w] + v)
        return table[num_items][capacity]

    def greedy(self, value_weight, capacity):
        value_weight.sort(key=lambda x: x[0]/x[1], reverse=True)
        total_value = 0
        total_weight = 0
        for v, w in value_weight:
            if total_weight + w <= capacity:
                total_value += v
                total_weight += w
            else:
                break
        return total_value
              

if __name__ == "__main__":
    kp = KP()
    kp.kp()
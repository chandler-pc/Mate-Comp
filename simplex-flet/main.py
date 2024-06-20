import flet as ft
import matplotlib.pyplot as plt
import numpy as np

class SimplexManager:
    number_variables = 0
    number_restrictions = 0
    max_min = "MAX"
    function = []
    restrictions = []
    restrictions_values = []
    simplex_table = []
    change_column = []
    change_column_value_min = []
    dual = False

def find_x_r(simplex_manager, index):
    for i in range(simplex_manager.number_restrictions):
        if simplex_manager.change_column[i] == "X"+str(index):
            return simplex_manager.simplex_table[i][-1]

def plot_graph(simplex_manager):
    x = np.linspace(0, 50, 100)
    
    for i in range(simplex_manager.number_restrictions):
        y = (simplex_manager.restrictions_values[i] - x * simplex_manager.restrictions[i][0]) / simplex_manager.restrictions[i][1]
        plt.plot(x, y, label=f'Restricción {i + 1}')
    Z_value = simplex_manager.simplex_table[-1][-1]
    x = -1*simplex_manager.simplex_table[-1][1] if simplex_manager.simplex_table[-1][1] != 0 else find_x_r(simplex_manager, 1)
    y = -1*simplex_manager.simplex_table[-1][2] if simplex_manager.simplex_table[-1][2] != 0 else find_x_r(simplex_manager, 2)
    plt.plot(x, y, 'ro', label=f'Z = {Z_value}')

    plt.xlim(0, 50)
    plt.ylim(0, 50)
    plt.xlabel("X1")
    plt.ylabel("X2")
    plt.title("Grafica de restricciones")
    plt.grid(True)
    plt.legend()
    plt.show()

def initial_page(page: ft.Page, simplex_manager: SimplexManager):
    def continue_button_click(e):
        simplex_manager.number_variables = int(
            number_of_variables_text_field.value)
        simplex_manager.number_restrictions = int(
            number_of_restrictions_text_field.value)
        simplex_manager.max_min = max_min_text_field.value
        page.clean()
        page.add(title)
        get_variables(page, simplex_manager)
    title = ft.Text(value="Calculadora Simplex",
                    style=ft.TextThemeStyle.DISPLAY_SMALL, text_align=ft.TextAlign.CENTER)
    continue_button = ft.ElevatedButton(
        text="Continuar",
        width=200,
        height=50,
        icon="arrow_forward",
        bgcolor="#B476FA",
        color="#000000",
        on_click=continue_button_click,
    )
    number_of_variables_text_field = ft.TextField(
        value="0", border_color="#ffffff", border_width=2, border_radius=5)
    number_of_restrictions_text_field = ft.TextField(
        value="0", border_color="#ffffff", border_width=2, border_radius=5)
    max_min_text_field = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option(key="MAX", text="Maximizar"),
            ft.dropdown.Option(key="MIN", text="Minimizar"),
            ft.dropdown.Option(key="DUAL", text="Dual")
        ],
        label="Problema de",
        value="MAX",
        border_color="#ffffff",
        border_width=2,
        border_radius=5,
        alignment=ft.alignment.center,
    )
    values = ft.Column(
        [
            ft.Container(
                padding=30,
            ),
            ft.Row(
                [
                    ft.Text(value="Ingrese el numero de variables : ",
                            style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
                    number_of_variables_text_field,
                ], alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(
                padding=30,
            ),
            ft.Row(
                [
                    ft.Text(value="Ingrese la cantidad de restricciones : ",
                            style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
                    number_of_restrictions_text_field,
                ], alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(
                padding=30,
            ),
            ft.Container(
                content=max_min_text_field,
                alignment=ft.alignment.center,
            ),
            ft.Container(
                padding=30,
            ),
            ft.Container(
                content=continue_button,
                alignment=ft.alignment.center,
            ),
        ]
    )
    page.add(title, values)

def get_variables(page: ft.Page, simplex_manager: SimplexManager):
    def continue_button_click(e):
        if simplex_manager.max_min == "DUAL":
            simplex_manager.dual = True
            simplex_manager.max_min = "MAX"
        for i in range(simplex_manager.number_variables):
            simplex_manager.function.append(
                float(function_row.controls[i*2].value))

        for i in range(simplex_manager.number_restrictions):
            simplex_manager.change_column.append(("S" if simplex_manager.max_min == "MAX" else "A") + str(i+1))
            simplex_manager.change_column_value_min.append(999999)
            simplex_manager.restrictions.append([])
            for j in range(simplex_manager.number_variables):
                simplex_manager.restrictions[i].append(
                    float(restrictions_column.controls[i].controls[j*2].value))
            simplex_manager.restrictions_values.append(float(
                restrictions_column.controls[i].controls[simplex_manager.number_variables*2 + 1].value))
        page.clean()
        if simplex_manager.dual:
            simplex_manager.number_variables, simplex_manager.number_restrictions = simplex_manager.number_restrictions, simplex_manager.number_variables
            simplex_manager.function, simplex_manager.restrictions_values = simplex_manager.restrictions_values, simplex_manager.function
            temp = []
            for i in range(len(simplex_manager.restrictions[0])):
                temp.append([])
                for j in range(len(simplex_manager.restrictions)):
                    temp[i].append(simplex_manager.restrictions[j][i])
            simplex_manager.restrictions = temp
            simplex_manager.change_column = []
            for i in range(simplex_manager.number_restrictions):
                simplex_manager.change_column.append("S"+str(i+1))
        print(simplex_manager.change_column)
        show_standard_form(page, simplex_manager)

    function_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    restrictions_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
    page_column = ft.Column(
        [
            ft.Container(
                padding=15,
                content=ft.Text(
                    value="Funcion Objetivo", style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
            ),
            function_row,
            ft.Container(
                padding=15,
                content=ft.Text(
                    value="Restricciones", style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
            ),
            restrictions_column,
            ft.Container(
                padding=15,
                content=ft.ElevatedButton(
                    text="Continuar",
                    width=200,
                    height=50,
                    icon="arrow_forward",
                    bgcolor="#B476FA",
                    color="#000000",
                    on_click=continue_button_click,
                ),
                alignment=ft.alignment.center,
            ),
        ],
        alignment=ft.alignment.center
    )
    safe_area = ft.SafeArea(
        content=page_column,
        expand=True,
        minimum=20,
    )

    for i in range(simplex_manager.number_variables):
        function_row.controls.append(ft.TextField(value="0", border_color="#ffffff", border_width=2,
                                     border_radius=5, width=70, height=40, text_align=ft.TextAlign.CENTER))
        function_row.controls.append(ft.Text(value="X"+str(i+1) + ("+" if i != simplex_manager.number_variables -
                                     1 else ""), style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER))

    for i in range(simplex_manager.number_restrictions):
        restrictions_column.controls.append(
            ft.Row(alignment=ft.MainAxisAlignment.CENTER))
        for j in range(simplex_manager.number_variables):
            restrictions_column.controls[i].controls.append(ft.TextField(
                value="0", border_color="#ffffff", border_width=2, border_radius=5, width=70, height=40, text_align=ft.TextAlign.CENTER))
            restrictions_column.controls[i].controls.append(ft.Text(value="X"+str(j+1) + (
                "+" if j != simplex_manager.number_variables-1 else ""), style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER))
        restrictions_column.controls[i].controls.append(
            ft.Text(value="≤" if simplex_manager.max_min == "MAX" else "≥",
                    style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)
        )
        restrictions_column.controls[i].controls.append(ft.TextField(
            value="0", border_color="#ffffff", border_width=2, border_radius=5, width=70, height=40, text_align=ft.TextAlign.CENTER))

    page.add(safe_area)

def show_standard_form(page: ft.Page, simplex_manager: SimplexManager):
    def continue_button_click(e):
        page.clean()
        show_simplex_table(page, simplex_manager)
    text_function = ""
    text_restrictions = ""
    if simplex_manager.max_min == "MAX":
        text_function = "Z"
        for i in range(simplex_manager.number_variables):
            text_function += " + " if simplex_manager.function[i] < 0 else " - " + str(
                simplex_manager.function[i]) + "X" + str(i+1) + (" " if i != simplex_manager.number_variables-1 else "")
        text_function += " = 0"
        for i in range(simplex_manager.number_restrictions):
            for j in range(simplex_manager.number_variables):
                text_restrictions += str(simplex_manager.restrictions[i][j]) + "X" + str(
                    j+1) + (" + " if j != simplex_manager.number_variables-1 else "")
            text_restrictions += " + S" + \
                str(i+1) + " = " + \
                str(simplex_manager.restrictions_values[i]) + "\n"
    if simplex_manager.max_min == "MIN":
        text_function = "Z = "
        for i in range(simplex_manager.number_variables):
            text_function += str(simplex_manager.function[i]) + "X" + \
                str(i+1) + (" + " if i != simplex_manager.number_variables-1 else "")
        for i in range(simplex_manager.number_restrictions):
            text_function += "+ 0" + "S" + str(i+1) +\
                " + MA" + \
                str(i+1)
        for i in range(simplex_manager.number_restrictions):
            for j in range(simplex_manager.number_variables):
                text_restrictions += str(simplex_manager.restrictions[i][j]) + "X" + str(
                    j+1) + (" + " if j != simplex_manager.number_variables-1 else "")
            text_restrictions += " - S" + \
                str(i+1) + " + A" + str(i+1) + " = " + \
                str(simplex_manager.restrictions_values[i]) + "\n"
    generate_simplex_table(simplex_manager)
    page.add(
        ft.Text(value="Forma Estandar", style=ft.TextThemeStyle.TITLE_LARGE,
                text_align=ft.TextAlign.CENTER),
        ft.Container(
            padding=30,
        ),
        ft.Text(value="Funcion Objetivo:", style=ft.TextThemeStyle.TITLE_LARGE,
                text_align=ft.TextAlign.CENTER),
        ft.Text(value=text_function, style=ft.TextThemeStyle.TITLE_LARGE,
                text_align=ft.TextAlign.CENTER),
        ft.Container(
            padding=30,
        ),
        ft.Text(value="Sujeto a:", style=ft.TextThemeStyle.TITLE_LARGE,
                text_align=ft.TextAlign.CENTER),
        ft.Text(value=text_restrictions, style=ft.TextThemeStyle.TITLE_LARGE,
                text_align=ft.TextAlign.CENTER),
        ft.Container(
            padding=30,
        ),
        ft.ElevatedButton(
            text="Calcular",
            width=200,
            height=50,
            icon="arrow_forward",
            bgcolor="#B476FA",
            color="#000000",
            on_click=continue_button_click,
        ),
    )

def generate_simplex_table(simplex_manager: SimplexManager):
    if simplex_manager.max_min == "MAX":
        for i in range(simplex_manager.number_restrictions):
            simplex_manager.simplex_table.append([])
            simplex_manager.simplex_table[i].append(0)
            for j in range(simplex_manager.number_variables):
                simplex_manager.simplex_table[i].append(
                    simplex_manager.restrictions[i][j])
            for j in range(simplex_manager.number_restrictions):
                simplex_manager.simplex_table[i].append(0 if i != j else 1)
            simplex_manager.simplex_table[i].append(
                simplex_manager.restrictions_values[i])
        simplex_manager.simplex_table.append([1])
        for i in range(simplex_manager.number_variables):
            simplex_manager.simplex_table[simplex_manager.number_restrictions].append(
                -1*simplex_manager.function[i])
        for i in range(simplex_manager.number_restrictions+1):
            simplex_manager.simplex_table[simplex_manager.number_restrictions].append(
                0)
    if simplex_manager.max_min == "MIN":
        for i in range(simplex_manager.number_restrictions):
            simplex_manager.simplex_table.append([])
            for j in range(simplex_manager.number_variables):
                simplex_manager.simplex_table[i].append(
                    simplex_manager.restrictions[i][j])
            for j in range(simplex_manager.number_restrictions):
                if j == i:
                    simplex_manager.simplex_table[i].append(-1)
                    simplex_manager.simplex_table[i].append(1)
                else:
                    simplex_manager.simplex_table[i].append(0)
                    simplex_manager.simplex_table[i].append(0)
            simplex_manager.simplex_table[i].append(
                simplex_manager.restrictions_values[i])
        simplex_manager.simplex_table.append([])
        for i in range(simplex_manager.number_variables):
            simplex_manager.simplex_table[simplex_manager.number_restrictions].append(
                simplex_manager.function[i])
        for i in range(simplex_manager.number_restrictions*2):
            simplex_manager.simplex_table[simplex_manager.number_restrictions].append(0 if i % 2 == 0 else 'M')
        simplex_manager.simplex_table[simplex_manager.number_restrictions].append(' ')

def show_simplex_table(page: ft.Page, simplex_manager: SimplexManager):
    def continue_button_click(e):
        page.clean()
        if simplex_manager.max_min == "MAX":
            calculate_simplex_max(simplex_manager)
            for i in range(simplex_manager.number_variables):
                if simplex_manager.simplex_table[simplex_manager.number_restrictions][i+1] < 0:
                    show_simplex_table(page, simplex_manager)
                    return
            show_final_table_max(page, simplex_manager)
        if simplex_manager.max_min == "MIN":
            calculate_simplex_min(simplex_manager)
            for i in range(simplex_manager.number_variables + simplex_manager.number_restrictions*2):
                    value = simplex_manager.simplex_table[simplex_manager.number_restrictions][i] if simplex_manager.simplex_table[simplex_manager.number_restrictions][i] != 'M' else 999999
                    for j in range(simplex_manager.number_restrictions):
                        value -= simplex_manager.simplex_table[j][i]*simplex_manager.change_column_value_min[j] 
                    if value < 0:
                        show_simplex_table(page, simplex_manager)
                        return
            show_final_table_min(page, simplex_manager)
        
    title = ft.Text(value="Tabla Simplex",
                    style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)
    simplex_datatable = None
    if simplex_manager.max_min == "MAX":
        simplex_datatable = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("*")),
                ft.DataColumn(ft.Text("Z"), numeric=True),
                *[ft.DataColumn(ft.Text("X"+str(i+1)), numeric=True)
                  for i in range(simplex_manager.number_variables)],
                *[ft.DataColumn(ft.Text("S"+str(i+1)), numeric=True)
                  for i in range(simplex_manager.number_restrictions)],
                ft.DataColumn(ft.Text("r"), numeric=True),
            ],
            rows=[
                *[ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(simplex_manager.change_column[i])),
                        *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[i][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions + 2)]]) for i in range(simplex_manager.number_restrictions)],
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Z")),
                        *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[simplex_manager.number_restrictions][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions + 2)]])
            ],
            border_radius=5,
        )
        
    if simplex_manager.max_min == "MIN":
        simplex_datatable = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("*")),
                *[ft.DataColumn(ft.Text("X"+str(i+1)), numeric=True)
                  for i in range(simplex_manager.number_variables)],
                *[ft.DataColumn(ft.Text(("S" if i % 2 == 0 else "A") +str((i%2)+1)), numeric=True) for i in range(simplex_manager.number_restrictions*2)],
                ft.DataColumn(ft.Text("r"), numeric=True),
            ],
            rows=[
                *[ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(simplex_manager.change_column[i])),
                        *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[i][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions*2 + 1)]]) for i in range(simplex_manager.number_restrictions)],
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Z")),
                        *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[simplex_manager.number_restrictions][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions*2 + 1)]])
            ],
            border_radius=5,
        )
    page.add(ft.SafeArea(
        content=ft.Column(
            [
                title,
                simplex_datatable,
                ft.Container(
                    padding=30,
                    content=ft.ElevatedButton(
                        text="Calcular",
                        width=200,
                        height=50,
                        icon="arrow_forward",
                        bgcolor="#B476FA",
                        color="#000000",
                        on_click=continue_button_click,
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
            alignment=ft.alignment.center,
        ), minimum=40))
    
    plot_graph(simplex_manager)

def calculate_simplex_max(simplex_manager: SimplexManager):
    pivot_column = 0
    pivot_row = 0
    pivot = float("inf")
    max_z = float("-inf")
    for i in range(len(simplex_manager.simplex_table[simplex_manager.number_restrictions])-1):
        if simplex_manager.simplex_table[simplex_manager.number_restrictions][i] < 0 and abs(simplex_manager.simplex_table[simplex_manager.number_restrictions][i]) > max_z:
            max_z = abs(simplex_manager.simplex_table[simplex_manager.number_restrictions][i])
            pivot_column = i
    min_r = float("inf")
    acoted = False
    for i in range(simplex_manager.number_restrictions):
        if simplex_manager.simplex_table[i][pivot_column] > 0:
            if simplex_manager.simplex_table[i][simplex_manager.number_variables + simplex_manager.number_restrictions + 1] / simplex_manager.simplex_table[i][pivot_column] < min_r:
                min_r = simplex_manager.simplex_table[i][simplex_manager.number_variables +
                                                         simplex_manager.number_restrictions + 1] / simplex_manager.simplex_table[i][pivot_column]
                pivot_row = i
                acoted = True
    if not acoted:
        print("No se puede acotar")
        return
    simplex_manager.change_column[pivot_row] = "X"+str(pivot_column)
    pivot = simplex_manager.simplex_table[pivot_row][pivot_column]
    for i in range(len(simplex_manager.simplex_table[pivot_row])):
        simplex_manager.simplex_table[pivot_row][i] /= pivot
    for i in range(len(simplex_manager.simplex_table)):
        if i != pivot_row:
            pivot = simplex_manager.simplex_table[i][pivot_column]
            for j in range(len(simplex_manager.simplex_table[i])):
                simplex_manager.simplex_table[i][j] -= pivot * \
                    simplex_manager.simplex_table[pivot_row][j]
    return

def calculate_simplex_min(simplex_manager: SimplexManager):
    temp = []
    pivot_column = 0
    pivot_row = 0
    pivot = 0
    for j in range(simplex_manager.number_variables+simplex_manager.number_restrictions*2):
        value = simplex_manager.simplex_table[simplex_manager.number_restrictions][j]
        if value == 'M':
            value = 999999
        temp.append(value - sum([simplex_manager.simplex_table[i][j]*simplex_manager.change_column_value_min[i] for i in range(simplex_manager.number_restrictions)]))
    min = float("inf")
    for i in range(len(temp)):
        if temp[i] < min:
            min = temp[i]
            pivot_column = i
    min_r = float("inf")
    acoted = False
    for i in range(simplex_manager.number_restrictions):
        if simplex_manager.simplex_table[i][pivot_column] > 0:
            if simplex_manager.simplex_table[i][simplex_manager.number_variables + simplex_manager.number_restrictions*2] / simplex_manager.simplex_table[i][pivot_column] < min_r:
                min_r = simplex_manager.simplex_table[i][simplex_manager.number_variables +
                                                         simplex_manager.number_restrictions*2] / simplex_manager.simplex_table[i][pivot_column]
                pivot_row = i
                acoted = True
    if not acoted:
        print("No se puede acotar")
        return
    pivot = simplex_manager.simplex_table[pivot_row][pivot_column]
    simplex_manager.change_column[pivot_row] = "X"+str(pivot_column+1)
    simplex_manager.change_column_value_min[pivot_row] = simplex_manager.simplex_table[simplex_manager.number_restrictions][pivot_column]
    for i in range(len(simplex_manager.simplex_table[pivot_row])):
        simplex_manager.simplex_table[pivot_row][i] /= pivot
    for i in range(simplex_manager.number_restrictions):
        if i != pivot_row:
            pivot = simplex_manager.simplex_table[i][pivot_column]
            for j in range(len(simplex_manager.simplex_table[i])):
                simplex_manager.simplex_table[i][j] -= pivot * \
                    simplex_manager.simplex_table[pivot_row][j]
    return

def show_final_table_max(page: ft.Page, simplex_manager: SimplexManager):
    title = ft.Text(value="Tabla Simplex Final",
                    style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)
    simplex_datatable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("*")),
            ft.DataColumn(ft.Text("Z"), numeric=True),
            *[ft.DataColumn(ft.Text("X"+str(i+1)), numeric=True)
              for i in range(simplex_manager.number_variables)],
            *[ft.DataColumn(ft.Text("S"+str(i+1)), numeric=True)
              for i in range(simplex_manager.number_restrictions)],
            ft.DataColumn(ft.Text("r"), numeric=True),
        ],
        rows=[
            *[ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(simplex_manager.change_column[i])),
                    *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[i][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions + 2)]]) for i in range(simplex_manager.number_restrictions)],
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Z")),
                    *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[simplex_manager.number_restrictions][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions + 2)]])
        ],
        border_radius=5,
    )
    values = []
    for i in range(len(simplex_manager.change_column)):
        values.append(
            f"{simplex_manager.change_column[i]} = {simplex_manager.simplex_table[i][simplex_manager.number_variables + simplex_manager.number_restrictions + 1]}")
    page.add(ft.SafeArea(
        content=ft.Column(
            [
                title,
                ft.Text(value="Maximizar",
                        style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
                simplex_datatable,
                ft.Text(value="El valor optimo es: " + str(simplex_manager.simplex_table[simplex_manager.number_restrictions][simplex_manager.number_variables +
                        simplex_manager.number_restrictions + 1]), style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
                *[ft.Text(value=f"{i}", style=ft.TextThemeStyle.TITLE_LARGE,
                          text_align=ft.TextAlign.CENTER) for i in values],
            ],
            expand=True,
            alignment=ft.alignment.center,
        ), minimum=40))
    plot_graph(simplex_manager)
    
def show_final_table_min(page: ft.Page, simplex_manager: SimplexManager):
    title = ft.Text(value="Tabla Simplex Final",
                    style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER)
    simplex_datatable = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("*")),
                *[ft.DataColumn(ft.Text("X"+str(i+1)), numeric=True)
                  for i in range(simplex_manager.number_variables)],
                *[ft.DataColumn(ft.Text(("S" if i % 2 == 0 else "A") +str((i%2)+1)), numeric=True) for i in range(simplex_manager.number_restrictions*2)],
                ft.DataColumn(ft.Text("r"), numeric=True),
            ],
            rows=[
                *[ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(simplex_manager.change_column[i])),
                        *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[i][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions*2 + 1)]]) for i in range(simplex_manager.number_restrictions)],
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Z")),
                        *[ft.DataCell(ft.Text(value=str(simplex_manager.simplex_table[simplex_manager.number_restrictions][j]), text_align=ft.TextAlign.CENTER)) for j in range(simplex_manager.number_variables + simplex_manager.number_restrictions*2 + 1)]])
            ],
            border_radius=5,
        )
    values = [0 for i in range(len(simplex_manager.function))]
    optim = 0
    for i in range(len(simplex_manager.change_column)):
        x_value = int(simplex_manager.change_column[i][1:])
        values[i]=f"{simplex_manager.change_column[x_value-1]} = {simplex_manager.simplex_table[x_value-1][simplex_manager.number_variables + simplex_manager.number_restrictions*2]}"
        optim += simplex_manager.function[x_value-1] * simplex_manager.simplex_table[i][simplex_manager.number_variables + simplex_manager.number_restrictions*2]
    page.add(ft.SafeArea(
        content=ft.Column(
            [
                title,
                ft.Text(value="Minimizar",
                        style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
                simplex_datatable,
                ft.Text(value="El valor optimo es: " + str(optim), style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
                *[ft.Text(value=f"{i}", style=ft.TextThemeStyle.TITLE_LARGE,
                          text_align=ft.TextAlign.CENTER) for i in values],
            ],
            expand=True,
            alignment=ft.alignment.center,
        ), minimum=40))


def main(page: ft.Page):
    page.window_height = 700
    page.window_width = 1000
    page.window_resizable = False
    page.window_full_screen = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.title = "Calculadora"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_center()
    page.window_visible = True
    simplex_manager = SimplexManager()
    initial_page(page, simplex_manager)


ft.app(target=main, view=ft.AppView.FLET_APP_HIDDEN)

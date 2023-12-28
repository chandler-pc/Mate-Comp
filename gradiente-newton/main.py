import flet as ft
import sympy as sp


def format_point(arr):
    point = "( "
    for i in range(len(arr)):
        point += str(arr[i]) + " ,"
    point = point[:-2]
    point += " )"
    return point


def format_theta(point1, point2):
    theta = "( "
    for i in range(len(point1)):
        theta += str(point1[i]) + " + " + str(point2[i]) + " * θ ,"
    theta = theta[:-2]
    theta += " )"
    return theta


def theta_to_function(expr_function, string_parameter):
    string_parameter = string_parameter.split(",")
    string_parameter[0] = string_parameter[0][1:]
    string_parameter[-1] = string_parameter[-1][:-1]
    for key, value in dict(zip("xyz", string_parameter)).items():
        expr_function = expr_function.replace(key, "(" + value + ")")
    return expr_function


def compare_points_variance(point1, point2, tolerance):
    for i in range(len(point1)):
        if abs(point1[i] - point2[i]) > tolerance:
            return False
    return True


class Manager:
    function = None
    expresion = None
    vars = []
    actual_point = []
    grad_exprs = []
    max_min = "max"

    def set_function(self, new_function, expresion):
        self.function = new_function
        self.expresion = expresion
        self.function(1, 1, 1, expr=expresion)

    def calculate_derivate(self):
        self.vars_symbols = []
        self.grad_function = []
        for i in range(len(self.vars)):
            self.vars_symbols.append(sp.symbols(self.vars[i]))
        if len(self.vars) == 1:
            exprs = str(self.function(
                self.vars_symbols[0], expr=self.expresion).diff(self.vars_symbols[0]))
            self.grad_exprs.append(exprs)
        if len(self.vars) == 2:
            for i in range(len(self.vars)):
                exprs = str(self.function(
                    self.vars_symbols[0], self.vars_symbols[1], expr=self.expresion).diff(self.vars_symbols[i]))
                self.grad_exprs.append(exprs)
        if len(self.vars) == 3:
            for i in range(len(self.vars)):
                exprs = str(self.function(
                    self.vars_symbols[0], self.vars_symbols[1], self.vars_symbols[2], expr=self.expresion).diff(self.vars_symbols[i]))
                self.grad_exprs.append(exprs)


manager = Manager()


def initial_page(page: ft.Page):
    def continue_to_calculate_gradient(e):
        if len(manager.actual_point) == 0:
            manager.actual_point = [0] * len(manager.vars)
        manager.max_min = select_max_min.value
        page.clean()
        calculate_page_gradient(page)

    def continue_to_calculate_newton(e):
        if len(manager.actual_point) == 0:
            manager.actual_point = [0] * len(manager.vars)
        manager.max_min = select_max_min.value
        page.clean()
        calculate_page_newton(page)

    def calculate_variables(e):
        if select_max_min.value == "max":
            expresion = "-1 * (" + e.control.value + ")"
        else:
            expresion = e.control.value
        manager.expresion = expresion
        try:
            funcion_lambda = lambda *args, expr: eval(
                expr, {**dict(zip('xyz', args)), **vars(sp)})
            manager.set_function(funcion_lambda, expresion)
            error_text.visible = False
            info_text.value = "Variables : "
            manager.vars = []
            for i in range(len(expresion)):
                if expresion[i] in "xyz" and expresion[i] not in manager.vars:
                    info_text.value += expresion[i] + " "
                    manager.vars.append(expresion[i])
            info_text.value = info_text.value[:-1]
            info_text.visible = True
            calculate_button_gradient.disabled = False
            calculate_button_newton.disabled = False
        except Exception as error:
            # print(error)
            error_text.visible = True
            error_text.value = "Error : Expresion no valida"
            info_text.visible = False
            calculate_button_gradient.disabled = True
            calculate_button_newton.disabled = True
        finally:
            show_initial_points()
            page.update()

    def calculate_variables_maxmin(e):
        if select_max_min.value == "max":
            expresion = "-1 * (" + function_input.value + ")"
        else:
            expresion = function_input.value
        manager.expresion = expresion
        try:
            funcion_lambda = lambda *args, expr: eval(
                expr, {**dict(zip('xyz', args)), **vars(sp)})
            manager.set_function(funcion_lambda, expresion)
            error_text.visible = False
            info_text.value = "Variables : "
            manager.vars = []
            for i in range(len(expresion)):
                if expresion[i] in "xyz" and expresion[i] not in manager.vars:
                    info_text.value += expresion[i] + " "
                    manager.vars.append(expresion[i])
            info_text.value = info_text.value[:-1]
            info_text.visible = True
            calculate_button_gradient.disabled = False
            calculate_button_newton.disabled = False
        except Exception as error:
            # print(error)
            error_text.visible = True
            error_text.value = "Error : Expresion no valida"
            info_text.visible = False
            calculate_button_gradient.disabled = True
            calculate_button_newton.disabled = True
        finally:
            show_initial_points()
            page.update()

    def show_initial_points():
        initial_points.controls = []
        for i in range(len(manager.vars)):
            initial_points.controls.append(ft.Row(
                controls=[
                    ft.Text(value=manager.vars[i] + "0",
                            style=ft.TextThemeStyle.BODY_LARGE),
                    ft.TextField(value="0", width=100, height=50, border_color="#ffffff",
                                 border_width=2, border_radius=5, text_align=ft.TextAlign.CENTER, on_change=set_initial_point)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            ))

    def set_initial_point(e):
        try:
            manager.actual_point = []
            for i in range(len(manager.vars)):
                manager.actual_point.append(
                    float(initial_points.controls[i].controls[1].value))
            error_text_points.visible = False
        except Exception as e:
            error_text_points.visible = True
            error_text_points.value = "Error : " + str(e)
        finally:
            page.update()

    title = ft.Text(value="Calculadora Gradiente - Newton",
                    style=ft.TextThemeStyle.DISPLAY_SMALL, text_align=ft.TextAlign.CENTER)
    function_input = ft.TextField(value="", width=300, height=70, border_color="#ffffff",
                                  border_width=2, border_radius=5, text_align=ft.TextAlign.CENTER, on_change=calculate_variables)
    error_text = ft.Text(value="Error: Escribe una funcion",
                         style=ft.TextThemeStyle.BODY_LARGE)
    info_text = ft.Text(value="Variables : ",
                        style=ft.TextThemeStyle.BODY_LARGE)
    info_text.visible = False
    initial_points = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER, spacing=30)
    show_initial_points()
    error_text_points = ft.Text(
        value="Error: ", style=ft.TextThemeStyle.BODY_LARGE)
    error_text_points.visible = False
    calculate_button_gradient = ft.ElevatedButton(text="Calcular Gradiente", width=200, height=50,
                                                  color="#B476FA", on_click=continue_to_calculate_gradient)
    calculate_button_newton = ft.ElevatedButton(text="Calcular Newton", width=200, height=50,
                                                color="#B476FA", on_click=continue_to_calculate_newton)
    calculate_button_gradient.disabled = True
    calculate_button_newton.disabled = True
    select_max_min = ft.Dropdown(
        options=[
            ft.dropdown.Option(key="max", text="Maximizar"),
            ft.dropdown.Option(key="min", text="Minimizar")
        ],
        value="max",
        width=200,
        height=55,
        on_change=calculate_variables_maxmin
    )
    page.add(ft.SafeArea(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    title,
                    ft.Row(
                        controls=[ft.Text(value="Ingrese la funcion a evaluar", style=ft.TextThemeStyle.BODY_LARGE),
                                  function_input],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    error_text,
                    info_text,
                    initial_points,
                    error_text_points,
                    select_max_min,
                    ft.Row(
                        controls=[
                            calculate_button_gradient,
                            calculate_button_newton
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=30
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            )
        ),
        minimum=30
    ))


def calculate_page_gradient(page: ft.Page):
    def calculate_iterations():
        counter = 0
        max_iterations = 100
        err = 0.0001
        while True:
            p = manager.actual_point
            exprs = [str(eval(manager.grad_exprs[i], {
                **dict(zip('xyz', p)), **vars(sp)
            })) for i in range(len(manager.vars))]
            theta_values = format_theta(p, exprs)
            theta_function = theta_to_function(manager.expresion, theta_values)
            theta_derivate = str(sp.diff(theta_function, "θ"))
            theta_derivate_doble = str(sp.diff(theta_derivate, "θ"))
            v = sp.solve(theta_derivate, "θ")
            theta = 0
            theta = theta if len(v) == 0 else v[0]
            theta = float(theta)
            new_point = [p[i] + theta * eval(exprs[i], {
                **dict(zip('xyz', p)), **vars(sp)
            }) for i in range(len(manager.vars))]
            IterationsText.controls.append(ft.Text(
                value="Iteracion " + str(counter + 1) + " : " + str(p), style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(value=manager.max_min + " g(θ) = f( " + format_point(
                p) + " + θ * " + format_point(exprs) + " )", style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(
                value="g(θ) = f" + theta_values, style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(
                value="g(θ) = " + theta_function, style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(
                value="g'(θ) = " + theta_derivate, style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(
                value="g''(θ) = " + theta_derivate_doble, style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(
                ft.Text(value="θ = " + str(theta), style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(
                value="Punto siguiente : " + str(new_point), style=ft.TextThemeStyle.HEADLINE_SMALL))
            if compare_points_variance(new_point, p, err):
                IterationsText.controls.append(ft.Text(
                    value="Punto minimo : " + str(new_point), style=ft.TextThemeStyle.HEADLINE_SMALL))
                break
            else:
                if counter == max_iterations:
                    IterationsText.controls.clear()
                    IterationsText.controls.append(
                        ft.Text(value="Maximas Iteraciones", style=ft.TextThemeStyle.HEADLINE_SMALL))
                    IterationsText.controls.append(ft.Text(
                        value="Punto minimo de la maxima iteracion : " + str(new_point), style=ft.TextThemeStyle.HEADLINE_SMALL))
                    break
                manager.actual_point = new_point
            counter += 1
            page.update()
    page.clean()
    manager.calculate_derivate()
    grad_str = "( "
    for i in range(len(manager.grad_exprs)):
        grad_str += str(manager.grad_exprs[i]) + " , "
    grad_str = grad_str[:-2]
    grad_str += ")"
    GF = ft.Text(value=" ▽f = " + grad_str,
                 style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    IterationsText = ft.Column(
        controls=[
            ft.Text(value="Iteraciones : ",
                    style=ft.TextThemeStyle.HEADLINE_SMALL)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30,
    )
    initial_point = manager.actual_point
    calculate_iterations()
    page.add(ft.SafeArea(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value="Funcion : " + manager.expresion,
                            style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Text(value="Gradiente de la funcion",
                            style=ft.TextThemeStyle.DISPLAY_SMALL),
                    GF,
                    ft.Text(value="Punto inicial : " + format_point(initial_point),
                            style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Text(value=manager.max_min + " g(θ) = f(X + θ▽f(X))",
                            style=ft.TextThemeStyle.HEADLINE_SMALL),
                    IterationsText
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30,
                scroll=ft.ScrollMode.ALWAYS,
                width=800,
                height=500
            ),
            expand=True
        ),
        expand=True,
        minimum=30
    ))


def calculate_page_newton(page: ft.Page):
    def calculate_iterations():
        counter = 0
        max_iterations = 100
        new_point = []
        while True:
            p = manager.actual_point
            exprs = [str(eval(manager.grad_exprs[i], {
                **dict(zip('xyz', p)), **vars(sp)
            })) for i in range(len(manager.vars))]
            H = []
            for i in range(len(manager.vars)):
                H.append([])
                for j in range(len(manager.vars)):
                    H[i].append(
                        str(sp.diff(manager.grad_exprs[i], manager.vars[j])))
                    H[i][j] = eval(H[i][j], {
                        **dict(zip('xyz', p)), **vars(sp)
                    })
            H_m = sp.Matrix(H)
            inv_H = H_m.inv()
            grad_matrix = []
            p_m = sp.Matrix(p)
            for i in range(len(manager.vars)):
                grad_matrix.append(eval(exprs[i], {
                    **dict(zip('xyz', p)), **vars(sp)
                }))
            grad_matrix_m = sp.Matrix(grad_matrix)
            new_point = p_m - inv_H * grad_matrix_m
            new_point = [float(new_point[i]) for i in range(len(new_point))]
            IterationsText.controls.append(ft.Text(
                value="Iteracion " + str(counter + 1) + " : " + format_point(p), style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(
                ft.Text(value="Hessiano : ", style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(
                value=(H), style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(
                ft.Text(value="Gradiente : ", style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(
                ft.Text(value=format_point(grad_matrix), style=ft.TextThemeStyle.HEADLINE_SMALL))
            IterationsText.controls.append(ft.Text(
                value="Punto siguiente : " + format_point(new_point), style=ft.TextThemeStyle.HEADLINE_SMALL))
            if compare_points_variance(new_point, p, 0.0001):
                IterationsText.controls.append(ft.Text(
                    value="Punto minimo : " + format_point(new_point), style=ft.TextThemeStyle.HEADLINE_SMALL))
                break
            else:
                if counter == max_iterations:
                    IterationsText.controls.clear()
                    IterationsText.controls.append(
                        ft.Text(value="Maximas Iteraciones", style=ft.TextThemeStyle.HEADLINE_SMALL))
                    break
                manager.actual_point = new_point
            counter += 1
            page.update()
    page.clean()
    manager.calculate_derivate()
    grad_str = "( "
    for i in range(len(manager.grad_exprs)):
        grad_str += str(manager.grad_exprs[i]) + " , "
    grad_str = grad_str[:-2]
    grad_str += ")"
    GF = ft.Text(value=" ▽f = " + grad_str,
                 style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    IterationsText = ft.Column(
        controls=[
            ft.Text(value="Iteraciones : ",
                    style=ft.TextThemeStyle.HEADLINE_SMALL)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30,
    )
    initial_point = manager.actual_point
    calculate_iterations()
    page.add(ft.SafeArea(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value="Funcion : " + manager.expresion,
                            style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Text(value="Gradiente de la funcion",
                            style=ft.TextThemeStyle.DISPLAY_SMALL),
                    GF,
                    ft.Text(value="Punto inicial : " + format_point(initial_point),
                            style=ft.TextThemeStyle.HEADLINE_SMALL),
                    IterationsText
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30,
                scroll=ft.ScrollMode.ALWAYS,
                width=800,
                height=500
            ),
            expand=True
        ),
        expand=True,
        minimum=30
    ))


def main(page: ft.Page):
    page.window_height = 700
    page.window_width = 1000
    page.window_resizable = False
    page.window_full_screen = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.title = "Metodo de Gradiente"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_center()
    page.window_visible = True
    initial_page(page)


ft.app(target=main, view=ft.AppView.FLET_APP_HIDDEN)

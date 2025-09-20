import tkinter as tk
import math

# --- Variables globales para modos ---
modo_f2_activo = False  # Modo Científico 1
modo_f3_activo = False  # Modo Científico 2
insertando_en_funcion = False  # Bandera: estamos dentro de una función con paréntesis


# --- Función auxiliar para factorial ---
def factorial(n):
    if n < 0:
        raise ValueError("Factorial no definido para negativos")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


# --- Función principal que maneja clics ---
def on_click(event):
    global modo_f2_activo, modo_f3_activo, insertando_en_funcion
    button_text = event.widget.cget("text")  # Texto del botón clicado
    current_text = entry.get()

    # --- Conmutadores de modos ---
    if button_text == "F2":
        modo_f2_activo = not modo_f2_activo  # Toggle ON/OFF
        return
    elif button_text == "F3":
        modo_f3_activo = not modo_f3_activo  # Toggle ON/OFF
        return

    # --- Limpiar pantalla ---
    if button_text == "C":
        entry.delete(0, tk.END)
        insertando_en_funcion = False
        return

    # --- Evaluar expresión ---
    if button_text == "=":
        try:
            expression = current_text

            # Reemplazos para funciones matemáticas
            replacements = {
                "sin(": "math.sin(",
                "cos(": "math.cos(",
                "tan(": "math.tan(",
                "asin(": "math.asin(",
                "acos(": "math.acos(",
                "atan(": "math.atan(",
                "log(": "math.log10(",
                "ln(": "math.log(",
                "√(": "math.sqrt(",
                "∛(": "lambda x: x**(1/3)(",  # raíz cúbica
                "π": "math.pi",
                "e": "math.e",
                "rad(": "math.radians(",
                "deg(": "math.degrees(",
                "^(": "(",
            }

            # Factorial: reemplazar "n!" por "factorial(n)"
            while "!" in expression:
                idx = expression.index("!")
                j = idx - 1
                while j >= 0 and (expression[j].isdigit() or expression[j] == "."):
                    j -= 1
                num_str = expression[j + 1:idx]
                expression = expression[:j + 1] + f"factorial({num_str})" + expression[idx + 1:]

            # Aplicar reemplazos
            for key, val in replacements.items():
                expression = expression.replace(key, val)

            # Evaluar expresión
            result = eval(expression)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
            insertando_en_funcion = False  # reiniciar
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
        return

    # --- Manejo dinámico de modos en teclas numéricas ---
    if button_text in "7894561230":
        if modo_f2_activo:  # Modo Científico 1
            mapping_f2 = {
                "7": "sin()",
                "8": "cos()",
                "9": "tan()",
                "4": "asin()",
                "5": "acos()",
                "6": "atan()",
                "1": "log()",
                "2": "ln()",
                "3": "π",
                "0": "e",
            }
            val = mapping_f2.get(button_text, button_text)
            entry.insert(tk.END, val)
            if val.endswith("()"):
                entry.icursor(entry.index(tk.END) - 1)
                insertando_en_funcion = True
            return

        if modo_f3_activo:  # Modo Científico 2
            mapping_f3 = {
                "7": "^(",
                "8": "√()",
                "9": "∛()",
                "4": "!(",
                "5": "rad()",
                "6": "deg()",
            }
            val = mapping_f3.get(button_text, button_text)
            entry.insert(tk.END, val)
            if val.endswith("()"):
                entry.icursor(entry.index(tk.END) - 1)
                insertando_en_funcion = True
            return

    # --- Caso especial: botón √ ---
    if button_text == "√":
        entry.insert(tk.END, "√()")
        entry.icursor(entry.index(tk.END) - 1)
        insertando_en_funcion = True
        return

    # --- Caso normal: insertar texto del botón ---
    if insertando_en_funcion and button_text.isdigit():
        # Si estamos dentro de paréntesis de función, insertar justo antes del ")"
        pos_cierre = entry.get().rfind(")")
        entry.insert(pos_cierre, button_text)
    else:
        entry.insert(tk.END, button_text)


# --- Ventana principal ---
root = tk.Tk()
root.title("Calculadora de Miguelinho")

# --- Caja de entrada ---
entry = tk.Entry(root, font=("Helvetica", 20))
entry.grid(row=0, column=0, columnspan=4)

# --- Lista de botones ---
buttons = [
    "7", "8", "9", "/",   # Fila 1
    "4", "5", "6", "*",   # Fila 2
    "1", "2", "3", "-",   # Fila 3
    "0", ".", "=", "+",   # Fila 4
    "C", "√", "F2", "F3"  # Fila 5
]

# --- Crear botones ---
row, col = 1, 0
for text in buttons:
    button = tk.Button(root, text=text, font=("Helvetica", 20), padx=20, pady=20)
    button.grid(row=row, column=col)
    button.bind("<Button-1>", on_click)

    col += 1
    if col > 3:
        col = 0
        row += 1

# --- Iniciar aplicación ---
root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import math

# --- SECCIÓN DE LÓGICA MATEMÁTICA ---

def euler(f, x0, y0, h, xn):
    resultados = []
    x, y = x0, y0
    n = 0
    # Añadimos el valor inicial
    resultados.append((n, round(x, 4), round(y, 6), round(f(x, y), 6)))
    
    while x < xn - h/2: # El -h/2 evita un paso extra por errores de redondeo decimal
        y = y + h * f(x, y)
        x = x + h
        n += 1
        resultados.append((n, round(x, 4), round(y, 6), round(f(x, y), 6)))
    return resultados

def euler_mejorado(f, x0, y0, h, xn):
    resultados = []
    x, y = x0, y0
    n = 0
    # Añadimos el valor inicial (no hay Yn* previo, lo dejamos vacío)
    resultados.append((n, round(x, 4), "-", round(y, 6)))
    
    while x < xn - h/2:
        y_pred = y + h * f(x, y) # Esto es Yn*
        y_corr = y + (h/2) * (f(x, y) + f(x + h, y_pred)) # Esto es el nuevo Yn
        x = x + h
        y = y_corr
        n += 1
        resultados.append((n, round(x, 4), round(y_pred, 6), round(y_corr, 6)))
    return resultados

def runge_kutta_4(f, x0, y0, h, xn):
    resultados = []
    x, y = x0, y0
    n = 0
    # Añadimos el valor inicial
    resultados.append((n, round(x, 4), "-", "-", "-", "-", round(y, 6)))
    
    while x < xn - h/2:
        k1 = f(x, y)
        k2 = f(x + h/2, y + (h * k1)/2)
        k3 = f(x + h/2, y + (h * k2)/2)
        k4 = f(x + h, y + (h * k3))
        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        x = x + h
        n += 1
        resultados.append((n, round(x, 4), round(k1, 6), round(k2, 6), round(k3, 6), round(k4, 6), round(y, 6)))
    return resultados

# --- SECCIÓN DE INTERFAZ GRÁFICA (GUI) ---

class AppMetodos:
    def __init__(self, root):
        self.root = root
        self.root.title("Iterador de Métodos Numéricos")
        self.root.geometry("700x600") # Ventana más ancha para las tablas

        # Contenedor de variables de entrada
        frame_inputs = tk.Frame(root)
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Ecuación f(x, y):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_f = tk.Entry(frame_inputs, width=25)
        self.entry_f.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="x0 (Valor inicial):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_x0 = tk.Entry(frame_inputs, width=15)
        self.entry_x0.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_inputs, text="y0 (Valor inicial):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_y0 = tk.Entry(frame_inputs, width=15)
        self.entry_y0.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_inputs, text="h (Tamaño de paso):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_h = tk.Entry(frame_inputs, width=15)
        self.entry_h.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_inputs, text="x final (Evaluar hasta):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_xn = tk.Entry(frame_inputs, width=15)
        self.entry_xn.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_inputs, text="Selecciona el Método:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.combo_metodo = ttk.Combobox(frame_inputs, values=["Euler", "Euler Mejorado", "Runge-Kutta 4"], state="readonly")
        self.combo_metodo.set("Euler")
        self.combo_metodo.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.btn_calcular = tk.Button(root, text="Calcular Tabla", command=self.ejecutar_calculo, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_calcular.pack(pady=10)

        # --- Área de la Tabla de Resultados (Treeview) ---
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        # Barra de desplazamiento
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, show="headings", yscrollcommand=self.scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.tree.yview)

    def ejecutar_calculo(self):
        try:
            # 1. Obtener datos de la interfaz
            func_str = self.entry_f.get()
            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            h = float(self.entry_h.get())
            xn = float(self.entry_xn.get())
            metodo = self.combo_metodo.get()

            # 2. Crear la función evaluable de forma segura
            f = lambda x, y: eval(func_str, {"x": x, "y": y, "math": math, "__builtins__": {}})

            # 3. Limpiar tabla anterior
            self.tree.delete(*self.tree.get_children())

            # 4. Configurar columnas y calcular según el método
            if metodo == "Euler":
                cols = ("n", "Xn", "Yn", "f(Xn, Yn)")
                res = euler(f, x0, y0, h, xn)
            elif metodo == "Euler Mejorado":
                cols = ("n", "Xn", "Yn*", "Yn")
                res = euler_mejorado(f, x0, y0, h, xn)
            else:
                cols = ("n", "Xn", "K1", "K2", "K3", "K4", "Yn")
                res = runge_kutta_4(f, x0, y0, h, xn)

            # Asignar nuevas columnas a la tabla
            self.tree["columns"] = cols
            for col in cols:
                self.tree.heading(col, text=col)
                # Ajustar el ancho de las columnas (la 'n' es más pequeña)
                ancho = 50 if col == "n" else 80
                self.tree.column(col, width=ancho, anchor=tk.CENTER)

            # 5. Insertar los nuevos resultados en la tabla
            for fila in res:
                self.tree.insert("", tk.END, values=fila)

        except Exception as e:
            messagebox.showerror("Error", f"Verifica los datos ingresados.\nPor favor, revisa la sintaxis de la ecuación.\nDetalle: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMetodos(root)
    root.mainloop()
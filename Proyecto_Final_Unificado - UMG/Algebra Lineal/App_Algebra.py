import tkinter as tk
from tkinter import ttk, messagebox
from inversa import matriz_inversa
from multiplicacion import multiplicar_matrices
from sistemas import gauss_jordan, regla_de_cramer
from excel_manager import guardar_resultado
import numpy as np


def formatear_matriz(matriz):
    def fmt(v):
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        else:
            return f"{v:.4f}".rstrip('0').rstrip('.')
    if isinstance(matriz, (list, np.ndarray)):
        return "\n".join(["| " + "   ".join(fmt(v) for v in fila) + " |" for fila in matriz])
    else:
        return str(matriz)


# principal
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Final - Álgebra Lineal")
        self.geometry("1000x650")
        self.configure(bg="#eef2f5")

       
        style = ttk.Style(self)
        style.theme_use("clam")
        azul_principal = "#0066cc"
        azul_oscuro = "#004c99"
        gris_fondo = "#eef2f5"
        gris_texto = "#343a40"
        blanco = "#ffffff"
        style.configure("TButton",
                        font=("Segoe UI Semibold", 11),
                        padding=8,
                        background=azul_principal,
                        foreground="white",
                        borderwidth=0)
        style.map("TButton",
                  background=[("active", azul_oscuro)],
                  relief=[("pressed", "groove")])

        style.configure("TLabel",
                        background=gris_fondo,
                        foreground=gris_texto,
                        font=("Segoe UI", 11))
        style.configure("Title.TLabel",
                        font=("Segoe UI Semibold", 20),
                        background=gris_fondo,
                        foreground=gris_texto)
        style.configure("SubTitle.TLabel",
                        font=("Segoe UI Italic", 12),
                        background=gris_fondo,
                        foreground="#555")

        self.columnconfigure(1, weight=1)
        self.menu_frame = tk.Frame(self, bg="#1e293b", width=240)
        self.menu_frame.grid(row=0, column=0, sticky="ns")
        self.content_frame = tk.Frame(self, bg=gris_fondo)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        ttk.Label(
            self.menu_frame,
            text="🧮  Menú Principal",
            background="#1e293b",
            foreground="white",
            font=("Segoe UI Semibold", 14)
        ).pack(pady=(25, 20))
        botones = [
            ("Inversa de Matriz", self.abrir_inversa),
            ("Multiplicación de Matrices", self.abrir_multiplicacion),
            ("Sistemas de Ecuaciones", self.abrir_sistemas),
        ]

        for texto, comando in botones:
            btn = tk.Button(
                self.menu_frame,
                text=texto,
                command=comando,
                bg="#334155",
                fg="white",
                activebackground=azul_principal,
                activeforeground="white",
                font=("Segoe UI", 11),
                relief="flat",
                padx=12,
                pady=10,
                width=25,
                anchor="w"
            )
            btn.pack(pady=7, padx=15)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#475569"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#334155"))

        self.mostrar_inicio()

#  inicio 
    def mostrar_inicio(self):
        self.limpiar_contenido()
        card = tk.Frame(self.content_frame, bg="white", bd=0, relief="solid", padx=30, pady=30)
        card.pack(pady=60, ipadx=10, ipady=10)

        ttk.Label(card, text="Proyecto Final - Álgebra Lineal", style="Title.TLabel").pack(pady=10)
        ttk.Label(card,
                  text="Seleccione una operación en el menú lateral para comenzar.",
                  style="SubTitle.TLabel").pack(pady=5)
# limpiar
    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

# resultados 
    def _open_result_window(self, title, text):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("650x450")
        win.configure(bg="#f8fafc")

        ttk.Label(win, text=title, style="Title.TLabel").pack(pady=10)

        frame = ttk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        txt = tk.Text(frame, wrap="none", font=("Consolas", 11),
                      bg="white", relief="solid", bd=1, height=15)
        txt.insert("1.0", text)
        txt.config(state=tk.DISABLED)
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ysb = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
        ysb.pack(side=tk.RIGHT, fill=tk.Y)
        txt.config(yscrollcommand=ysb.set)

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        def copiar():
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Copiado", "Resultado copiado al portapapeles.")

        def guardar():
            guardar_resultado("resultados_algebra.xlsx", "Resultados", [text])
            messagebox.showinfo("Guardado", "Resultado guardado en resultados_algebra.xlsx")

        ttk.Button(btn_frame, text="📋 Copiar", command=copiar).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="💾 Guardar", command=guardar).pack(side=tk.LEFT, padx=6)

# Inversa
    def abrir_inversa(self):
        self.limpiar_contenido()
        ttk.Label(self.content_frame, text="Cálculo de Inversa de Matriz", style="Title.TLabel").pack(pady=10)
        ttk.Label(self.content_frame, text="Ingrese la matriz (filas separadas por Enter, columnas por espacio):").pack()

        ejemplo = tk.Frame(self.content_frame, bg="#dbeafe", bd=1, relief="solid", padx=12, pady=8)
        ejemplo.pack(pady=8)
        tk.Label(ejemplo, text="Ejemplo:\n2 1\n7 4", bg="#dbeafe", font=("Consolas", 11)).pack()
        tk.Label(ejemplo, text="(Separe columnas con espacio y cada fila con Enter)", bg="#dbeafe",
                 font=("Arial", 9, "italic")).pack()

        self.txt_matriz = tk.Text(self.content_frame, height=6, width=55, font=("Consolas", 11), relief="solid", bd=1)
        self.txt_matriz.pack(pady=8)

        ttk.Button(self.content_frame, text="Calcular Inversa", command=self.calcular_inversa).pack(pady=12)

    def calcular_inversa(self):
        try:
            texto = self.txt_matriz.get("1.0", tk.END).strip()
            A = [list(map(float, fila.split())) for fila in texto.splitlines()]
            inv = matriz_inversa(A)
            guardar_resultado("resultados_algebra.xlsx", "Inversas", [str(A), str(inv)])
            resultado = f"Matriz A:\n{formatear_matriz(A)}\n\nInversa:\n{formatear_matriz(inv)}"
            self._open_result_window("Inversa de Matriz", resultado)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Multiplicación 
    def abrir_multiplicacion(self):
        self.limpiar_contenido()
        ttk.Label(self.content_frame, text="Multiplicación de Matrices", style="Title.TLabel").pack(pady=10)

        ejemplo = tk.Frame(self.content_frame, bg="#fff3cd", bd=1, relief="solid", padx=12, pady=8)
        ejemplo.pack(pady=8)
        tk.Label(ejemplo, text="Ejemplo de matriz A:\n1 2\n3 4", bg="#fff3cd", font=("Consolas", 11)).pack()
        tk.Label(ejemplo, text="Ejemplo de matriz B:\n5 6\n7 8", bg="#fff3cd", font=("Consolas", 11)).pack()
        tk.Label(ejemplo, text="(El número de columnas de A debe igualar las filas de B)", bg="#fff3cd",
                 font=("Arial", 9, "italic")).pack()

        ttk.Label(self.content_frame, text="Matriz A:").pack()
        self.txt_A = tk.Text(self.content_frame, height=5, width=55, font=("Consolas", 11), relief="solid", bd=1)
        self.txt_A.pack(pady=6)

        ttk.Label(self.content_frame, text="Matriz B:").pack()
        self.txt_B = tk.Text(self.content_frame, height=5, width=55, font=("Consolas", 11), relief="solid", bd=1)
        self.txt_B.pack(pady=6)

        ttk.Button(self.content_frame, text="Multiplicar", command=self.calcular_multiplicacion).pack(pady=12)

    def calcular_multiplicacion(self):
        try:
            A = [list(map(float, fila.split())) for fila in self.txt_A.get("1.0", tk.END).strip().splitlines()]
            B = [list(map(float, fila.split())) for fila in self.txt_B.get("1.0", tk.END).strip().splitlines()]
            res = multiplicar_matrices(A, B)
            guardar_resultado("resultados_algebra.xlsx", "Multiplicaciones", [str(A), str(B), str(res)])
            resultado = f"Matriz A:\n{formatear_matriz(A)}\n\nMatriz B:\n{formatear_matriz(B)}\n\nResultado:\n{formatear_matriz(res)}"
            self._open_result_window("Multiplicación de Matrices", resultado)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Sistemas 
    def abrir_sistemas(self):
        self.limpiar_contenido()
        ttk.Label(self.content_frame, text="Resolución de Sistemas de ecuaciones", style="Title.TLabel").pack(pady=10)

        ejemplo = tk.Frame(self.content_frame, bg="#d1fae5", bd=1, relief="solid", padx=12, pady=8)
        ejemplo.pack(pady=8)
        tk.Label(ejemplo, text="Ejemplo de A:\n2 -1\n1 3", bg="#d1fae5", font=("Consolas", 11)).pack()
        tk.Label(ejemplo, text="Ejemplo de b:\n3 7", bg="#d1fae5", font=("Consolas", 11)).pack()
        tk.Label(ejemplo, text="(Cada fila en A es una ecuación; b son los resultados)", bg="#d1fae5",
                 font=("Arial", 9, "italic")).pack()

        ttk.Label(self.content_frame, text="Coeficientes de la matriz A:").pack()
        self.txt_A_sys = tk.Text(self.content_frame, height=5, width=55, font=("Consolas", 11), relief="solid", bd=1)
        self.txt_A_sys.pack(pady=5)

        ttk.Label(self.content_frame, text="Vector b (separado por espacios):").pack()
        self.txt_b_sys = tk.Entry(self.content_frame, width=55, font=("Consolas", 11), relief="solid", bd=1)
        self.txt_b_sys.pack(pady=5)

        ttk.Label(self.content_frame, text="Método:").pack()
        self.metodo = ttk.Combobox(self.content_frame, values=["Gauss-Jordan", "Regla de Cramer"], state="readonly")
        self.metodo.current(0)
        self.metodo.pack(pady=5)

        ttk.Button(self.content_frame, text="Resolver Sistema", command=self.calcular_sistema).pack(pady=12)

    def calcular_sistema(self):
        try:
            A = np.array([list(map(float, fila.split())) for fila in self.txt_A_sys.get("1.0", tk.END).strip().splitlines()])
            b = np.array(list(map(float, self.txt_b_sys.get().split())))

            if self.metodo.get() == "Gauss-Jordan":
                x = gauss_jordan(A, b)
            else:
                x = regla_de_cramer(A, b)

            if isinstance(x, (int, float, np.floating)):
                x = [[float(x)]]
            elif isinstance(x, np.ndarray) and x.ndim == 1:
                x = [[float(v)] for v in x]

            guardar_resultado("resultados_algebra.xlsx", "Sistemas", [self.metodo.get(), str(A), str(b), str(x)])
            resultado = f"Matriz A:\n{formatear_matriz(A)}\n\nVector b:\n{b}\n\nSolución ({self.metodo.get()}):\n{formatear_matriz(x)}"
            self._open_result_window("Sistema de Ecuaciones", resultado)
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()

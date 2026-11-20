import tkinter as tk
from tkinter import messagebox
from datos import MATERIAS_CREDITOS, cargar_alumnos, guardar_alumnos
from logica import (
    validar_id_nuevo,
    validar_materias_seleccionadas,
    buscar_alumno,
    eliminar_alumno,
    calcular_promedio_ponderado,
)


class AppPonderador:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ponderador Académico")
        self.root.geometry("400x460")
        self.alumnos = cargar_alumnos()
        self._construir_menu_principal()

    def _construir_menu_principal(self):
        tk.Label(self.root, text="Sistema de Promedio Ponderado", font=("Arial", 12, "bold")).pack(pady=15)

        marco = tk.Frame(self.root, bg="light blue", padx=25, pady=20)
        marco.pack(padx=20, pady=10, fill="both", expand=True)

        botones = [
            ("1. Registrar alumno", self.abrir_registro_id),
            ("2. Calcular promedio ponderado", self.abrir_selector_alumno),
            ("3. Eliminar registro por ID", self.abrir_eliminar_alumno),
            ("4. Resetear registros", self.resetear_datos),
            ("5. Salir", self.salir),
        ]
        for texto, accion in botones:
            tk.Button(marco, text=texto, width=28, command=accion).pack(pady=9)

    def abrir_registro_id(self):
        ventana_id = tk.Toplevel(self.root)
        ventana_id.title("Registrar ID")
        ventana_id.geometry("360x150")

        marco = tk.Frame(ventana_id, bg="light blue", padx=20, pady=20)
        marco.pack(fill="both", expand=True)

        tk.Label(marco, text="ID del alumno:", bg="light blue").grid(row=0, column=0, padx=5, pady=10)
        entrada_id = tk.Entry(marco, width=20)
        entrada_id.grid(row=0, column=1, padx=5, pady=10)
        entrada_id.focus()

        def continuar(event=None):
            try:
                id_valido = validar_id_nuevo(entrada_id.get(), self.alumnos)
            except ValueError as error:
                messagebox.showerror("ID inválido", str(error), parent=ventana_id)
                return
            ventana_id.destroy()
            self._abrir_seleccion_materias(id_valido)

        entrada_id.bind("<Return>", continuar)
        tk.Button(marco, text="Continuar", command=continuar).grid(row=1, column=0, columnspan=2, pady=10)

    def _abrir_seleccion_materias(self, id_alumno: str):
        ventana_mat = tk.Toplevel(self.root)
        ventana_mat.title(f"Materias - {id_alumno}")
        ventana_mat.geometry("420x420")

        marco = tk.Frame(ventana_mat, bg="light blue", padx=20, pady=15)
        marco.pack(fill="both", expand=True)

        tk.Label(marco, text="Selecciona las materias cursadas:", bg="light blue", font=("Arial", 10, "bold")).pack(
            anchor="w", pady=(0, 10)
        )

        checks = {}
        for materia, creditos in MATERIAS_CREDITOS.items():
            var = tk.BooleanVar(value=False)
            checks[materia] = var
            tk.Checkbutton(
                marco,
                text=f"{materia} ({creditos} créd.)",
                variable=var,
                bg="light blue",
            ).pack(anchor="w", pady=3)

        def guardar():
            seleccionadas = [m for m, var in checks.items() if var.get()]
            try:
                validar_materias_seleccionadas(seleccionadas)
            except ValueError as error:
                messagebox.showerror("Selección inválida", str(error), parent=ventana_mat)
                return

            self.alumnos[id_alumno] = seleccionadas
            guardar_alumnos(self.alumnos)
            ventana_mat.destroy()
            messagebox.showinfo("Guardado", f"Alumno '{id_alumno}' registrado con {len(seleccionadas)} materias.")

        tk.Button(marco, text="Guardar materias", command=guardar).pack(pady=15)

    def abrir_selector_alumno(self):
        if not self.alumnos:
            messagebox.showwarning("Sin registros", "Primero debes registrar al menos un alumno.")
            return

        ventana_sel = tk.Toplevel(self.root)
        ventana_sel.title("Seleccionar Alumno")
        ventana_sel.geometry("340x360")

        marco = tk.Frame(ventana_sel, bg="light blue", padx=20, pady=20)
        marco.pack(fill="both", expand=True)

        tk.Label(marco, text="Elige un alumno:", bg="light blue", font=("Arial", 10, "bold")).pack(pady=(0, 10))

        for id_alumno in self.alumnos:
            tk.Button(
                marco,
                text=id_alumno,
                width=22,
                command=lambda aid=id_alumno: self._abrir_captura_calificaciones(ventana_sel, aid),
            ).pack(pady=5)

    def _abrir_captura_calificaciones(self, ventana_anterior: tk.Toplevel, id_alumno: str):
        ventana_anterior.destroy()
        ventana_cal = tk.Toplevel(self.root)
        ventana_cal.title(f"Calificaciones - {id_alumno}")
        ventana_cal.geometry("460x400")

        marco = tk.Frame(ventana_cal, bg="light blue", padx=20, pady=20)
        marco.pack(fill="both", expand=True)

        tk.Label(marco, text="Ingresa las calificaciones (0 a 10):", bg="light blue", font=("Arial", 10, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        entradas = {}
        for fila, materia in enumerate(self.alumnos[id_alumno], start=1):
            tk.Label(marco, text=materia, bg="light blue").grid(row=fila, column=0, sticky="w", padx=10, pady=6)
            caja = tk.Entry(marco, width=8)
            caja.grid(row=fila, column=1, padx=10, pady=6)
            entradas[materia] = caja

        def procesar():
            datos_capturados = {mat: caja.get() for mat, caja in entradas.items()}
            try:
                promedio = calcular_promedio_ponderado(datos_capturados)
            except ValueError as error:
                messagebox.showerror("Dato inválido", str(error), parent=ventana_cal)
                return

            messagebox.showinfo("Resultado", f"El promedio ponderado de {id_alumno} es: {promedio}", parent=ventana_cal)

        tk.Button(marco, text="Calcular Promedio", command=procesar).grid(
            row=len(entradas) + 1, column=0, columnspan=2, pady=15
        )

    def abrir_eliminar_alumno(self):
        if not self.alumnos:
            messagebox.showwarning("Sin registros", "No hay alumnos registrados para eliminar.")
            return

        ventana_del = tk.Toplevel(self.root)
        ventana_del.title("Eliminar Registro")
        ventana_del.geometry("380x160")

        marco = tk.Frame(ventana_del, bg="light blue", padx=20, pady=20)
        marco.pack(fill="both", expand=True)

        tk.Label(marco, text="ID a eliminar:", bg="light blue").grid(row=0, column=0, padx=5, pady=10)
        entrada_id = tk.Entry(marco, width=22)
        entrada_id.grid(row=0, column=1, padx=5, pady=10)
        entrada_id.focus()

        def buscar_y_eliminar(event=None):
            try:
                id_encontrado, materias = buscar_alumno(entrada_id.get(), self.alumnos)
            except ValueError as error:
                messagebox.showerror("Búsqueda sin resultados", str(error), parent=ventana_del)
                return

            lista_materias = ", ".join(materias)
            confirmado = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Eliminar el registro del alumno '{id_encontrado}'?\n\nMaterias inscritas: {lista_materias}",
                parent=ventana_del,
            )
            if confirmado:
                eliminar_alumno(id_encontrado, self.alumnos)
                guardar_alumnos(self.alumnos)
                ventana_del.destroy()
                messagebox.showinfo("Registro eliminado", f"El alumno '{id_encontrado}' fue eliminado correctamente.")

        entrada_id.bind("<Return>", buscar_y_eliminar)
        tk.Button(marco, text="Buscar y eliminar", command=buscar_y_eliminar).grid(
            row=1, column=0, columnspan=2, pady=10
        )

    def resetear_datos(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar todos los alumnos registrados?"):
            self.alumnos.clear()
            guardar_alumnos(self.alumnos)
            messagebox.showinfo("Reseteo", "Todos los registros han sido eliminados.")

    def salir(self):
        messagebox.showinfo("Hasta luego", "Gracias por usar el sistema.")
        self.root.destroy()
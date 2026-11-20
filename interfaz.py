"""Interfaz del programa."""
import tkinter as tk
from tkinter import messagebox, simpledialog

from datos import alumnos, materias
from alumnos import (
    registrar_alumno,
    agregar_materia_alumno,
    eliminar_materia_alumno
)
from materias import (
    agregar_materia,
    eliminar_materia,
    cambiar_creditos
)
from promedios import calcular_promedio


def iniciar():
    """Crea la pantalla de inicio."""
    ventana = tk.Tk()
    ventana.title("Los Tuntunsitos")
    ventana.geometry("470x510")
    ventana.configure(bg="#EAF0F6")
    ventana.resizable(False, False)

    # --------------------------------
    # FUNCIONES DE LA INTERFAZ
    # --------------------------------

    def mostrar_promedio():

        id_a = simpledialog.askinteger(
            "Promedio",
            "Ingrese el ID del alumno:",
            parent=ventana
        )

        if id_a is None:
            return

        if id_a not in alumnos:
            messagebox.showerror(
                "Error", "Alumno no registrado"
            )
            return

        calificaciones = {}

        for m in alumnos[id_a]:

            if m not in materias:
                continue

            nota = simpledialog.askfloat(
                "Calificación",
                f"Ingrese el promedio de {m}:",
                minvalue=0,
                maxvalue=10,
                parent=ventana
            )

            if nota is None:
                return

            calificaciones[m] = nota

        resultado = calcular_promedio(
            id_a, calificaciones
        )

        if resultado is not None:
            messagebox.showinfo(
                "Resultado",
                f"Tu promedio ponderado es: {resultado:.2f}"
            )
        else:
            messagebox.showerror(
                "Error",
                "No se pudo calcular el promedio"
            )

    def registrar():

        id_a = simpledialog.askinteger(
            "Registrar alumno",
            "Ingrese el ID del alumno:",
            parent=ventana
        )

        if id_a is None:
            return

        if registrar_alumno(id_a):
            messagebox.showinfo(
                "Registro",
                "Alumno registrado correctamente"
            )
        else:
            messagebox.showwarning(
                "Aviso",
                "El alumno ya está registrado"
            )

    def administrar_catalogo():

        opcion = simpledialog.askinteger(
            "Materias",
            "1. Agregar materia\n"
            "2. Eliminar materia\n"
            "3. Cambiar créditos\n\n"
            "Seleccione una opción:",
            minvalue=1,
            maxvalue=3,
            parent=ventana
        )

        if opcion is None:
            return

        if opcion == 1:

            nombre = simpledialog.askstring(
                "Agregar",
                "Nombre de la materia:",
                parent=ventana
            )

            if nombre is None:
                return

            nombre = nombre.strip().title()

            if not nombre:
                return

            credito = simpledialog.askinteger(
                "Créditos",
                "Ingrese los créditos:",
                minvalue=1,
                parent=ventana
            )

            if credito is None:
                return

            mensaje = agregar_materia(nombre, credito)

        elif opcion == 2:

            nombre = simpledialog.askstring(
                "Eliminar",
                "Ingrese el nombre exacto de la materia:",
                parent=ventana
            )

            if nombre is None:
                return

            mensaje = eliminar_materia(nombre.strip())

        else:

            nombre = simpledialog.askstring(
                "Créditos",
                "Ingrese el nombre exacto de la materia:",
                parent=ventana
            )

            if nombre is None:
                return

            credito = simpledialog.askinteger(
                "Créditos",
                "Ingrese los nuevos créditos:",
                minvalue=1,
                parent=ventana
            )

            if credito is None:
                return

            mensaje = cambiar_creditos(
                nombre.strip(), credito
            )

        messagebox.showinfo("Resultado", mensaje)

    def administrar_alumno():

        id_a = simpledialog.askinteger(
            "Alumno",
            "Ingrese el ID del alumno:",
            parent=ventana
        )

        if id_a is None:
            return

        if id_a not in alumnos:
            messagebox.showerror(
                "Error", "Alumno no registrado"
            )
            return

        opcion = simpledialog.askinteger(
            "Materias del alumno",
            "1. Agregar materia\n"
            "2. Eliminar materia\n\n"
            "Seleccione una opción:",
            minvalue=1,
            maxvalue=2,
            parent=ventana
        )

        if opcion is None:
            return

        if opcion == 1:

            nombre = simpledialog.askstring(
                "Inscribir",
                "Materias disponibles:\n" +
                "\n".join(materias.keys()) +
                "\n\nIngrese el nombre exacto:",
                parent=ventana
            )

            if nombre is None:
                return

            mensaje = agregar_materia_alumno(
                id_a, nombre.strip()
            )

        else:

            nombre = simpledialog.askstring(
                "Eliminar",
                "Materias inscritas:\n" +
                "\n".join(alumnos[id_a]) +
                "\n\nIngrese el nombre exacto:",
                parent=ventana
            )

            if nombre is None:
                return

            mensaje = eliminar_materia_alumno(
                id_a, nombre.strip()
            )

        messagebox.showinfo("Resultado", mensaje)

    def mostrar_informacion():

        texto = "MATERIAS DISPONIBLES\n\n"

        for m, c in materias.items():
            texto += f"{m}: {c} créditos\n"

        texto += "\nALUMNOS REGISTRADOS\n\n"

        for id_a, lista in alumnos.items():
            texto += f"ID: {id_a}\n"

            for m in lista:
                texto += f"- {m}\n"

            texto += "\n"

        messagebox.showinfo(
            "Información",
            texto
        )

    # --------------------------------
    # DISEÑO DE LA VENTANA
    # --------------------------------

    titulo = tk.Label(
        ventana,
        text="LOS TUNTUNSITOS",
        font=("Arial", 22, "bold"),
        bg="#243B53",
        fg="white",
        pady=20
    )
    titulo.pack(fill="x")

    subtitulo = tk.Label(
        ventana,
        text="Sistema de control académico",
        font=("Arial", 11),
        bg="#EAF0F6",
        fg="#243B53"
    )
    subtitulo.pack(pady=15)

    def crear_boton(texto, funcion):

        tk.Button(
            ventana,
            text=texto,
            command=funcion,
            font=("Arial", 10, "bold"),
            bg="#334E68",
            fg="white",
            width=38,
            height=2,
            cursor="hand2"
        ).pack(pady=5)

    crear_boton(
        "1. Mostrar promedio ponderado",
        mostrar_promedio
    )

    crear_boton(
        "2. Registrar alumno",
        registrar
    )

    crear_boton(
        "3. Modificar materias",
        administrar_catalogo
    )

    crear_boton(
        "4. Agregar / Eliminar materias del alumno",
        administrar_alumno
    )

    crear_boton(
        "5. Mostrar información del sistema",
        mostrar_informacion
    )

    crear_boton(
        "6. Salir",
        ventana.destroy
    )

    ventana.mainloop()

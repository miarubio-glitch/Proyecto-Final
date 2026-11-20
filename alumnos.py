"""Alumnos.

Este apartado registra los alumnos, agrega las materias a los alumnos,
y eliminar las materias de un alumno.
"""

from datos import alumnos, materias


def registrar_alumno(id_a):
    """Registrar un alumno en el programa."""
    if id_a in alumnos:
        return False
    alumnos[id_a] = []
    return True


def agregar_materia_alumno(id_a, materia):
    """Agregar un materia en el alumno."""
    if id_a not in alumnos:
        return "Alumno no registrado"

    if materia not in materias:
        return "Materia no disponible"

    if materia in alumnos[id_a]:
        return "Materia ya inscrita"

    alumnos[id_a].append(materia)
    return "Materia agregada correctamente"


def eliminar_materia_alumno(id_a, materia):
    """Eliminar un materia en el alumno."""
    if id_a not in alumnos:
        return "Alumno no registrado"

    if materia not in alumnos[id_a]:
        return "Materia no inscrita"

    alumnos[id_a].remove(materia)
    return "Materia eliminada correctamente"

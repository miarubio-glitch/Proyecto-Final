"""Materias.

En enta clase se modifican las materias.
"""
from datos import materias, alumnos


def agregar_materia(nombre, creditos):
    """Agregar una materia al menú."""
    if nombre in materias:
        return "La materia ya existe"
    if not nombre or creditos <= 0:
        return "Datos incorrectos"
    materias[nombre] = creditos
    return "Materia agregada correctamente"


def eliminar_materia(nombre):
    """Eliminar una materia."""
    if nombre not in materias:
        return "Materia no disponible"
    del materias[nombre]
    for id_a in alumnos:
        if nombre in alumnos[id_a]:
            alumnos[id_a].remove(nombre)
    return "Materia eliminada correctamente"


def cambiar_creditos(nombre, creditos):
    """Cambiar los creditos de una materia."""
    if nombre not in materias:
        return "Materia no disponible"
    if creditos <= 0:
        return "Los créditos deben ser positivos"
    materias[nombre] = creditos
    return "Créditos actualizados correctamente"

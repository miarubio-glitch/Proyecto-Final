"""Promedios.

En esta clase se calcula el promedio ponderado.
"""
from datos import alumnos, materias


def calcular_promedio(id_a, calificaciones):
    """Calcula el promedio de los alumnos."""
    if id_a not in alumnos:
        return None
    suma = 0
    total_creditos = 0
    for m in alumnos[id_a]:
        if m not in materias:
            continue
        if m not in calificaciones:
            return None
        promedio = calificaciones[m]
        if not 0 <= promedio <= 10:
            return None
        credito = materias[m]
        suma += promedio * credito
        total_creditos += credito
    if total_creditos > 0:
        return suma / total_creditos
    return None

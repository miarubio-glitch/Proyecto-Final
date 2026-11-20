from datos import MATERIAS_CREDITOS


def validar_id_nuevo(id_alumno: str, alumnos: dict[str, list[str]]) -> str:
    id_limpio = id_alumno.strip()
    if not id_limpio:
        raise ValueError("El ID del alumno no puede estar vacío.")
    if id_limpio in alumnos:
        raise ValueError(f"El ID '{id_limpio}' ya se encuentra registrado.")
    return id_limpio


def validar_materias_seleccionadas(materias: list[str]) -> list[str]:
    if not materias:
        raise ValueError("Debes seleccionar al menos una materia.")
    return materias


def buscar_alumno(id_alumno: str, alumnos: dict[str, list[str]]) -> tuple[str, list[str]]:
    id_limpio = id_alumno.strip()
    if not id_limpio:
        raise ValueError("Debes ingresar un ID para buscar.")
    if id_limpio not in alumnos:
        raise ValueError(f"No se encontró ningún alumno con el ID '{id_limpio}'.")
    return id_limpio, alumnos[id_limpio]


def eliminar_alumno(id_alumno: str, alumnos: dict[str, list[str]]) -> list[str]:
    id_limpio, _ = buscar_alumno(id_alumno, alumnos)
    return alumnos.pop(id_limpio)


def calcular_promedio_ponderado(calificaciones_texto: dict[str, str]) -> float:
    suma_ponderada = 0.0
    total_creditos = 0

    for materia, texto in calificaciones_texto.items():
        valor = texto.strip()
        if not valor:
            raise ValueError(f"Falta ingresar la calificación de '{materia}'.")
        try:
            calificacion = float(valor)
        except ValueError:
            raise ValueError(f"La calificación de '{materia}' debe ser un número válido.")

        if not (0.0 <= calificacion <= 10.0):
            raise ValueError(f"La calificación de '{materia}' debe estar entre 0 y 10.")

        creditos = MATERIAS_CREDITOS[materia]
        suma_ponderada += calificacion * creditos
        total_creditos += creditos

    if total_creditos == 0:
        raise ValueError("El alumno no tiene créditos asignados.")

    return round(suma_ponderada / total_creditos, 2)
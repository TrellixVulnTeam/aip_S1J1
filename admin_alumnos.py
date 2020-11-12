import requests


def solicitar_entero(mensaje, vacio=False):
    """
    Solicita al usuario que ingrese un número entero en pantalla y repite
    la acción hasta que el dato sea válido.
    Si `vacio` es `True`, solo se realiza el chequeo si el usuario ingresa
    algo. 
    """
    while True:
        dato = input(mensaje)
        if vacio and not dato:
            return None
        try:
            return int(dato)
        except ValueError:
            pass


print("1. Agregar un alumno.")
print("2. Modificar alumno existente.")
print("3. Listar alumnos.")
print("4. Eliminar un alumno.")
while True:
    opcion = input("Seleccione una opción: ")
    if opcion in "1234":
        break

url = "http://localhost:7001/student"

if opcion == "1":
    nombre = input("Nombre: ")
    cursos = solicitar_entero("Cursos: ")
    r = requests.post(url, json={"name": nombre, "courses": cursos})
    if r.status_code == 201:
        print("Alumno ingresado correctamente.")
    else:
        print("No se ha podido ingresar el alumno.")

elif opcion == "2":
    id_alumno = solicitar_entero("Ingrese el ID del alumno: ")
    datos = {}
    nombre = input("Nuevo nombre (o deje vacío para mantener el anterior): ")
    if nombre:
        datos["name"] = nombre
    cursos = solicitar_entero(
        "Nueva cantidad de cursos (o deje vacío): ", vacio=True)
    if cursos:
        datos["courses"] = cursos
    r = requests.put(url + f"/{id_alumno}", json=datos)
    if r.status_code == 204:
        print("Alumno modificado correctamente.")
    else:
        print("No se ha podido modificar el alumno.")

elif opcion == "3":
    r = requests.get(url)
    if r.status_code == 200:
        for alumno in r.json()["students"]:
            print(f'{alumno["id"]}. {alumno["name"]} ({alumno["courses"]} cursos).')
    else:
        print("No se pudo obtener la lista de alumnos.")

elif opcion == "4":
    id_alumno = solicitar_entero("Ingrese el ID del alumno: ")
    r = requests.delete(url + f"/{id_alumno}")
    if r.status_code == 204:
        print("Alumno eliminado correctamente.")
    else:
        print("No se pudo eliminar el alumno.")

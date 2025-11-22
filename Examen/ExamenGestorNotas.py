import pandas as pd
import csv
import os

NOMBRE_CSV = 'notas_alumnos.csv'
def registrar_alumno():
    print("*"*69," REGISTRAR NUEVO ALUMNO ","*"*70)
    nombre = input("Ingrese el nombre del alumno: ").strip().title()
    asignatura = input("Ingrese el nombre de la asignatura: ").strip().title()

    try:
        with open(NOMBRE_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nombre, asignatura])
        print(f"\n¡Alumno {nombre} registrado exitosamente!")
    except Exception as e:
        print(f"Ocurrió un error al guardar los datos: {e}")

def ingresar_notas():
    print("*"*65," INGRESO DE NOTAS Y PONDERACIONES ","*"*64)
    try:
        df = pd.read_csv(NOMBRE_CSV)
        if df.empty:
            print("No hay alumnos registrados. Use la Opción 1 primero.")
            return
    except FileNotFoundError:
        print(f"El archivo {NOMBRE_CSV} no existe.")
        return

    print("\nAlumnos registrados:")
    print(df['Nombre'].tolist())
    
    nombre_buscar = input("\nIngrese el nombre del alumno para ingresar notas: ").strip().title()
    
    if nombre_buscar not in df['Nombre'].values:
        print(f"Error: El alumno '{nombre_buscar}' no encontrado.")
        return

    while True:
        try:
            num_notas = int(input("¿Cuántas notas desea ingresar para este alumno? "))
            if num_notas > 0:
                break
            else:
                print("Debe ingresar al menos una nota.")
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")

    notas_dict = {}
    ponderaciones = []
    
    for i in range(1, num_notas + 1):
        while True:
            try:
                nota = float(input(f"Ingrese Nota {i} (1.0 a 7.0): "))
                if not (1.0 <= nota <= 7.0):
                    print("Error: La nota debe estar entre 1.0 y 7.0.")
                    continue
                
                ponderacion = int(input(f"Ingrese Ponderación para Nota {i} (en %): "))
                if not (0 <= ponderacion <= 100):
                    print("Error: La ponderación debe estar entre 0 y 100.")
                    continue
                
                notas_dict[f'Nota_{i}'] = nota
                ponderaciones.append(ponderacion)
                break
            except ValueError:
                print("Error: Entrada inválida. Ingrese números.")
    
    if sum(ponderaciones) != 100:
        print(f"\nAdvertencia: La suma de las ponderaciones es {sum(ponderaciones)}%. El promedio se calculará con esa base.")

    pesos = [p / 100 for p in ponderaciones]
    
    notas_lista = list(notas_dict.values())
    promedio_ponderado = sum(n * p for n, p in zip(notas_lista, pesos))
    
    for i, nota in enumerate(notas_lista):
        df.loc[df['Nombre'] == nombre_buscar, f'Nota_{i+1}'] = nota
        df.loc[df['Nombre'] == nombre_buscar, f'Peso_{i+1}'] = pesos[i]

    df.loc[df['Nombre'] == nombre_buscar, 'Promedio_Final'] = promedio_ponderado

    df.to_csv(NOMBRE_CSV, index=False)
    print(f"\nNotas y ponderación guardadas para {nombre_buscar}. Promedio: {promedio_ponderado:.2f}")

def main():    
    try:
        while True:
            print("")
            print ("-"*165)
            print ("="*72, 'MENÚ GESTOR DE NOTAS', "="*71)
            print ("-"*165)
            print ("-"*5,"Opcion 1. Ingreso de Alumnos"," "*124,"-"*5)
            print ("-"*5,"Opcion 2. Ingreso de Notas"," "*126,"-"*5)
            print ("-"*5,"Opcion 3. Busqueda por Nombre o Califiaciones en general (Aprobado/Desaprobado)"," "*73,"-"*5)
            print ("-"*5,"Opcion 4. Salir del programa"," "*124,"-"*5)
            print ("-"*165)
            print("")
            
            r = int(input("Ingrese una opcion (1, 2, 3 o 4): "))
            print("")

            if r==1:
                registrar_alumno()

            elif r==2:
                ingresar_notas()

            elif r == 3:
                print ("!Busqueda por Nombre o Califiaciones en general (Aprobado/Desaprobado)¡")


            elif r == 4:
                print ("Saliendo del programa...")
                break; 


            else:
                print("!Ingresa una opcion válida (1, 2, 3 o 4)¡");
    
    except:
        print("Error: !Ingresa una opcion valida¡")
        return 
main()

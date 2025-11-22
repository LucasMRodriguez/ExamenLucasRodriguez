import pandas as pd
import csv
import os

NOMBRE_CSV = 'notas_alumnos.csv'

def crear_csv_si_no_existe():
    if not os.path.exists(NOMBRE_CSV):
        print(f"Creando el archivo inicial: {NOMBRE_CSV}")
        with open(NOMBRE_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nombre', 'Asignatura'])


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
        print(f"\nAdvertencia: La suma de las ponderaciones es {sum(ponderaciones)}%. Debe ser de 100%")
        return
    
    pesos = [p / 100 for p in ponderaciones]
    
    notas_lista = list(notas_dict.values())
    promedio_ponderado = sum(n * p for n, p in zip(notas_lista, pesos))
    
    for i, nota in enumerate(notas_lista):
        df.loc[df['Nombre'] == nombre_buscar, f'Nota_{i+1}'] = nota
        df.loc[df['Nombre'] == nombre_buscar, f'Peso_{i+1}'] = pesos[i]

    df.loc[df['Nombre'] == nombre_buscar, 'Promedio_Final'] = promedio_ponderado

    df.to_csv(NOMBRE_CSV, index=False)
    print(f"\nNotas y ponderación guardadas para {nombre_buscar}. Promedio: {promedio_ponderado:.1f}")



def buscar_alumno_por_nombre(df):
    print("\nAlumnos registrados:")
    print(df['Nombre'].tolist())
    nombre_buscar = input("\nIngrese el nombre exacto del alumno a buscar: ").strip().title()
    
    resultado = df[df['Nombre'] == nombre_buscar]
    
    if resultado.empty:
        print(f"El alumno '{nombre_buscar}' no existe.")
        return
    
    promedio = resultado['Promedio_Final'].iloc[0]
    if pd.isna(promedio):
        print(f"Alumno '{nombre_buscar}' existe, pero aún NO tiene notas ni promedio final calculado.")
        return 


    print("")
    print ("="*85)
    print(f"- DETALLE DE NOTAS PARA {nombre_buscar.upper()}")
    notas_cols = [col for col in resultado.columns if col.startswith('Nota_')]
    pesos_cols = [col for col in resultado.columns if col.startswith('Peso_')]
    
    print(f"Asignatura: {resultado['Asignatura'].iloc[0]}")
    for i in range(len(notas_cols)):
        nota = resultado[notas_cols[i]].iloc[0]
        peso = resultado[pesos_cols[i]].iloc[0] * 100 
        
        if pd.notna(nota):
            print(f"  > {notas_cols[i]}: {nota:.1f} (Ponderación: {peso:.0f}%)")
    
    promedio = resultado['Promedio_Final'].iloc[0]
    estado = "APROBADO" if promedio >= 4.0 else "REPROBADO"
    
    print(f"\nPROMEDIO FINAL: {promedio:.1f}")
    print(f"ESTADO: {estado}")
    print ("="*85)

def calificaciones_generales(df):
    print("")
    print("="*20,"--- REPORTE DE CALIFICACIONES GENERALES ---","="*20)
    
    df_reporte = df.dropna(subset=['Promedio_Final']).copy()

    if df_reporte.empty:
        print("No hay promedios finales calculados para generar el reporte.")
        return

    promedio_general = df_reporte['Promedio_Final'].mean()
    print(f"Promedio General del Curso: {promedio_general:.1f}")

    umbral = 4.0
    df_reporte['Estado'] = df_reporte['Promedio_Final'].apply(lambda x: 'APROBADO' if x >= umbral else 'REPROBADO')

    conteo_estado = df_reporte['Estado'].value_counts()
    
    print("\n--- Resumen por Estado ---")
    print(conteo_estado)


    reprobados = df_reporte[df_reporte['Estado'] == 'REPROBADO']
    if not reprobados.empty:
        print("="*85)
        print("\nDetalle de Reprobados:")
        print(reprobados[['Nombre', 'Promedio_Final']].sort_values(by='Promedio_Final'))
    
    aprobados = df_reporte[df_reporte['Estado'] == 'APROBADO']
    if not aprobados.empty:
        print("")
        print("="*85)
        print("\nDetalle de Aprobados:")
        print(aprobados[['Nombre', 'Promedio_Final']].sort_values(by='Promedio_Final', ascending=False))
    print("")
    print("="*85)

def gestion_reportes():
    try:
        df = pd.read_csv(NOMBRE_CSV)
    except FileNotFoundError:
        print(f"El archivo {NOMBRE_CSV} no existe o no hay datos para generar reportes.")
        return

    while True:
        print("")
        print("*"*50,"--- GENERAR REPORTE ---","*"*50)
        print("1. Búsqueda por Nombre de Alumno")
        print("2. Calificaciones Generales (Aprobado/Reprobado)")
        print("3. Volver al Menú Principal")
        print ("*"*125)
        opcion_reporte = input("Seleccione una opción de reporte: ")

        if opcion_reporte == '1':
            buscar_alumno_por_nombre(df)

        elif opcion_reporte == '2':
            calificaciones_generales(df)
        
        elif opcion_reporte == '3':
            break

        else:
            print("Opción no válida. Intente de nuevo.")


def main():    
    crear_csv_si_no_existe()
    try:
        while True:
            print("")
            print ("-"*165)
            print ("="*72, 'MENÚ GESTOR DE NOTAS', "="*71)
            print ("-"*165)
            print ("-"*5,"Opcion 1. Ingreso de Alumnos"," "*124,"-"*5)
            print ("-"*5,"Opcion 2. Ingreso de Notas"," "*126,"-"*5)
            print ("-"*5,"Opcion 3. Busqueda por Nombre o Calificaciones en general (Aprobado/Desaprobado)"," "*72,"-"*5)
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
                gestion_reportes()

            elif r == 4:
                print ("Saliendo del programa...")
                break; 


            else:
                print("!Ingresa una opcion válida (1, 2, 3 o 4)¡");
    
    except:
        print("Error: !Ingresa una opcion valida¡")
        return 
main()

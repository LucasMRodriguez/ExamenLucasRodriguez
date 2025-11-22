#Importa la librería Pandas, esencial para la lectura, escritura y manipulación del CSV.
import pandas as pd

#Importa el módulo csv, utilizado para la escritura inicial del encabezado si el archivo no existe.
import csv

#Importa el módulo os, utilizado para verificar la existencia del archivo en el sistema de archivos.
import os

#Importa el módulo time, utilizado para generar una pequeña pausa antes de salir del programa.
import time

#Define el nombre del archivo CSV que se usará para la persistencia de datos.
NOMBRE_CSV = 'notas_alumnos.csv'

def crear_csv_si_no_existe(): #Función que verifica si el archivo CSV existe y si no existe, lo crea e inicializa con los encabezados básicos 
    if not os.path.exists(NOMBRE_CSV):
        print(f"Creando el archivo inicial: {NOMBRE_CSV}")
        #Abre el archivo en modo 'w' (escritura) y define 'newline='' para evitar líneas en blanco extra en Windows.
        with open(NOMBRE_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            #Escribe la primera fila con los encabezados iniciales.
            writer.writerow(['Nombre', 'Asignatura'])
            
def registrar_alumno(): #Función que ingresa a los alumnos.
    print("*"*69," REGISTRAR NUEVO ALUMNO ","*"*70)
    
    #Solicita el nombre y normaliza el texto (quita espacios, capitaliza).
    nombre = input("Ingrese el nombre del alumno: ").strip().title()
    asignatura = input("Ingrese el nombre de la asignatura: ").strip().title()

    try:
        #Intenta verificar si el alumno ya existe usando Pandas.
        try:
            #Lee el CSV completo.
            df = pd.read_csv(NOMBRE_CSV)

            #Lógica de validación: verifica si el nombre está en la columna NOMBRE.
            if nombre in df['Nombre'].values:
                print(f"\nError: El alumno '{nombre}' ya se encuentra registrado. No se agregó.")
                return #Detiene la función si el alumno ya existe.
        
        #Manejo de error si el archivo existe pero está vacío (no detiene el flujo).
        except:
            pass

        #Si no hubo duplicados, abre el archivo en modo 'a' (append/añadir) para agregar la fila.
        with open(NOMBRE_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            #Escribe la nueva fila con el nombre y la asignatura.
            writer.writerow([nombre, asignatura])
        
        print(f"\n¡Alumno {nombre} registrado exitosamente!")
        
    except Exception as e:
        print(f"Ocurrió un error al guardar los datos: {e}")


def ingresar_notas(): #Permite ingresar notas y sus ponderaciones a un alumno existentes, con condicionales.
    print("*"*65," INGRESO DE NOTAS Y PONDERACIONES ","*"*64)
    try:
        df = pd.read_csv(NOMBRE_CSV) #Carga el DataFrame
        if df.empty:
            print("No hay alumnos registrados. Use la Opción 1 primero.")
            return
    except FileNotFoundError:
        print(f"El archivo {NOMBRE_CSV} no existe.")
        return

    print("\nAlumnos registrados:")
    print(df['Nombre'].tolist())
    
    nombre_buscar = input("\nIngrese el nombre del alumno para ingresar notas: ").strip().title()
    
    #Valida que el alumno exista en el DataFrame
    if nombre_buscar not in df['Nombre'].values:
        print(f"Error: El alumno '{nombre_buscar}' no encontrado.")
        return

    #Ciclo de validación para el número de notas
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
    
    #Ciclo principal FOR para solicitar la nota y la ponderación por separado
    for i in range(1, num_notas + 1):
        while True: #Ciclo interno para validar la entrada de cada nota/ponderación
            try:
                #Solicita y valida el rango de la nota (1.0 a 7.0)
                nota = float(input(f"Ingrese Nota {i} (1.0 a 7.0): "))
                if not (1.0 <= nota <= 7.0):
                    print("Error: La nota debe estar entre 1.0 y 7.0.")
                    continue
                
                #Solicita y valida el rango de la ponderación (0 a 100)
                ponderacion = int(input(f"Ingrese Ponderación para Nota {i} (en %): "))
                if not (0 <= ponderacion <= 100):
                    print("Error: La ponderación debe estar entre 0 y 100.")
                    continue
                
                notas_dict[f'Nota_{i}'] = nota
                ponderaciones.append(ponderacion)
                break
            except ValueError:
                print("Error: Entrada inválida. Ingrese números.")
    
    #Validación de suma de ponderaciones (requisito de lógica)
    if sum(ponderaciones) != 100:
        print(f"\nAdvertencia: La suma de las ponderaciones es {sum(ponderaciones)}%. Debe ser de 100%")
        return #Termina la función si no suma 100%
    
    #Convierte las ponderaciones porcentuales a decimales (el peso)
    pesos = [p / 100 for p in ponderaciones]
    
    notas_lista = list(notas_dict.values())

    #Cálculo del promedio ponderado (lógica clave)
    promedio_ponderado = sum(n * p for n, p in zip(notas_lista, pesos))
    
    #Actualización del DataFrame con las nuevas columnas
    #Usa df.loc para localizar la fila del alumno y asignar las notas/pesos.
    for i, nota in enumerate(notas_lista):
        df.loc[df['Nombre'] == nombre_buscar, f'Nota_{i+1}'] = nota
        df.loc[df['Nombre'] == nombre_buscar, f'Peso_{i+1}'] = pesos[i]

    #Asigna el promedio final.
    df.loc[df['Nombre'] == nombre_buscar, 'Promedio_Final'] = promedio_ponderado

    #Guarda el DataFrame actualizado en el CSV.
    df.to_csv(NOMBRE_CSV, index=False)
    print(f"\nNotas y ponderación guardadas para {nombre_buscar}. Promedio: {promedio_ponderado:.1f}")


def eliminar_alumno(): #Permite eliminar un registro de alumno del CSV. Ademas pide confirmación antes de la eliminación irreversible.
    print("*"*67," ELIMINAR REGISTRO DE ALUMNO ","*"*67)
    try:
        df = pd.read_csv(NOMBRE_CSV)
        if df.empty:
            print("No hay alumnos registrados para eliminar.")
            return
    except FileNotFoundError:
        print(f"El archivo {NOMBRE_CSV} no existe.")
        return

    print("\nAlumnos registrados:")
    print(df['Nombre'].tolist())
    
    nombre_buscar = input("\nIngrese el nombre exacto del alumno a ELIMINAR: ").strip().title()
    
    #Identifica los índices de las filas a eliminar.
    indice_a_eliminar = df[df['Nombre'] == nombre_buscar].index
    
    if indice_a_eliminar.empty:
        print(f"Error: El alumno '{nombre_buscar}' no fue encontrado.")
        return

    confirmacion = input(f"¿Está seguro de eliminar a '{nombre_buscar}' y todos sus datos? (S/N): ").upper()
    
    if confirmacion == 'S' or confirmacion == 'SI':
        #Método drop() de Pandas para eliminar la fila.
        df_actualizado = df.drop(indice_a_eliminar)
        
        #Guarda el nuevo DataFrame sin la fila eliminada.
        df_actualizado.to_csv(NOMBRE_CSV, index=False)
        print(f"\n¡Alumno '{nombre_buscar}' eliminado exitosamente del sistema!")
    else:
        print(f"Eliminación de '{nombre_buscar}' cancelada.")


def buscar_alumno_por_nombre(df): #Muestra el detalle de notas, ponderaciones, promedio final y estado de un alumno.
    print("\nAlumnos registrados:")
    print(df['Nombre'].tolist())
    nombre_buscar = input("\nIngrese el nombre exacto del alumno a buscar: ").strip().title()
    
    #Filtra el DataFrame para obtener solo la fila del alumno.
    resultado = df[df['Nombre'] == nombre_buscar]
    
    if resultado.empty:
        print(f"El alumno '{nombre_buscar}' no existe.")
        return
    
    #Accede al valor del Promedio_Final.
    promedio = resultado['Promedio_Final'].iloc[0]

    #Comprueba si el promedio es NaN (no ha ingresado notas).
    if pd.isna(promedio):
        print(f"Alumno '{nombre_buscar}' existe, pero aún NO tiene notas ni promedio final calculado.")
        return 


    print("")
    print ("="*85)
    print(f"- DETALLE DE NOTAS PARA {nombre_buscar.upper()}")
    
    #Genera listas de columnas de notas y pesos para iterar solo sobre ellas.
    notas_cols = [col for col in resultado.columns if col.startswith('Nota_')]
    pesos_cols = [col for col in resultado.columns if col.startswith('Peso_')]
    
    print(f"Asignatura: {resultado['Asignatura'].iloc[0]}")
    #Ciclo para mostrar cada nota y su respectiva ponderación
    for i in range(len(notas_cols)):
        nota = resultado[notas_cols[i]].iloc[0]
        peso = resultado[pesos_cols[i]].iloc[0] * 100 #Convierte el peso a porcentaje
        
        if pd.notna(nota):
            print(f"  > {notas_cols[i]}: {nota:.1f} (Ponderación: {peso:.0f}%)")
    
    #Determina el estado de aprobación/reprobación.
    promedio = resultado['Promedio_Final'].iloc[0]
    estado = "APROBADO" if promedio >= 4.0 else "REPROBADO" #Uso del umbral 4.0
    
    print(f"\nPROMEDIO FINAL: {promedio:.1f}")
    print(f"ESTADO: {estado}")
    print ("="*85)


def editar_notas_alumno(): #Permite modificar una nota existente de un alumno y recalcula su promedio.

    print("*"*65," EDITAR NOTAS DEL ALUMNO ","*"*65)
    try:
        df = pd.read_csv(NOMBRE_CSV)
        if df.empty:
            print("No hay alumnos registrados.")
            return
    except FileNotFoundError:
        print(f"El archivo {NOMBRE_CSV} no existe.")
        return

    print("\nAlumnos registrados:")
    print(df['Nombre'].tolist())
    
    nombre_buscar = input("\nIngrese el nombre exacto del alumno para editar notas: ").strip().title()
    
    if nombre_buscar not in df['Nombre'].values:
        print(f"Error: El alumno '{nombre_buscar}' no fue encontrado.")
        return

    #Obtiene el índice de la fila del alumno
    indice_alumno = df[df['Nombre'] == nombre_buscar].index[0]

    #Identifica las notas que ya tienen un valor (no son NaN).
    notas_existentes = [col for col in df.columns if col.startswith('Nota_') and pd.notna(df.loc[indice_alumno, col])]
    
    if not notas_existentes:
        print(f"El alumno '{nombre_buscar}' existe, pero aún no tiene notas ingresadas.")
        return
    
    print(f"\nNotas existentes para {nombre_buscar}:")
    #Muestra las opciones de notas a editar
    for i, col_nota in enumerate(notas_existentes):
        col_peso = col_nota.replace('Nota_', 'Peso_')
        nota_actual = df.loc[indice_alumno, col_nota]
        peso_actual = df.loc[indice_alumno, col_peso] * 100
        print(f"{i+1}. {col_nota}: {nota_actual:.1f} (Peso: {peso_actual:.0f}%)")

    #Bucle para seleccionar la nota a editar.
    while True:
        try:
            seleccion = int(input("\nIngrese el número de la nota que desea editar: "))
            if 1 <= seleccion <= len(notas_existentes):
                columna_a_editar = notas_existentes[seleccion - 1]
                break
            else:
                print("Número de nota no válido.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

    #Bucle para solicitar y validar el nuevo valor de la nota.
    while True:
        try:
            nueva_nota = float(input(f"Ingrese el nuevo valor para {columna_a_editar} (1.0 a 7.0): "))
            if 1.0 <= nueva_nota <= 7.0:
                break
            else:
                print("Error: La nota debe estar entre 1.0 y 7.0.")
        except ValueError:
            print("Error: Entrada inválida. Ingrese un número.")
            
    #Actualiza el valor de la nota modificada en el DataFrame.
    df.loc[indice_alumno, columna_a_editar] = nueva_nota
    
    #Recálculo del promedio ponderado
    notas_finales = []
    pesos_finales = []
    
    #Itera sobre todas las columnas para recolectar las notas y pesos existentes.
    for col in df.columns:
        if col.startswith('Nota_') and pd.notna(df.loc[indice_alumno, col]):
            peso_col = col.replace('Nota_', 'Peso_')
            
            notas_finales.append(df.loc[indice_alumno, col])
            pesos_finales.append(df.loc[indice_alumno, peso_col])
            
    #Calcula el nuevo promedio.
    nuevo_promedio = sum(n * p for n, p in zip(notas_finales, pesos_finales))
    
    #Actualiza el Promedio_Final con el nuevo valor.
    df.loc[indice_alumno, 'Promedio_Final'] = nuevo_promedio
    
    #Guarda el DataFrame actualizado.
    df.to_csv(NOMBRE_CSV, index=False)
    print(f"\n¡{columna_a_editar} actualizada para {nombre_buscar}!")
    print(f"El nuevo promedio final es: {nuevo_promedio:.1f}")


def calificaciones_generales(df): #Genera reportes de resumen general: promedio del curso, conteo de aprobados/reprobados y detalle de cada grupo.

    print("")
    print("="*20,"--- REPORTE DE CALIFICACIONES GENERALES ---","="*20)
    
    #Crea una copia del DataFrame solo con alumnos que tienen Promedio_Final calculado.
    df_reporte = df.dropna(subset=['Promedio_Final']).copy()

    if df_reporte.empty:
        print("No hay promedios finales calculados para generar el reporte.")
        return

    #Cálculo del promedio general (uso de .mean() de Pandas).
    promedio_general = df_reporte['Promedio_Final'].mean()
    print(f"Promedio General del Curso: {promedio_general:.1f}")

    umbral = 4.0
    #Creación de una nueva columna 'Estado' usando una función lambda (filtro) de Pandas.
    df_reporte['Estado'] = df_reporte['Promedio_Final'].apply(lambda x: 'APROBADO' if x >= umbral else 'REPROBADO')

    #Conteo de ocurrencias por estado (uso de .value_counts() de Pandas).
    conteo_estado = df_reporte['Estado'].value_counts()
    
    print("\n--- Resumen por Estado ---")
    print(conteo_estado)


    #Filtra y muestra el detalle de los REPROBADOS (ordenados por promedio).
    reprobados = df_reporte[df_reporte['Estado'] == 'REPROBADO']
    if not reprobados.empty:
        print("="*85)
        print("\nDetalle de Reprobados:")
        print(reprobados[['Nombre', 'Promedio_Final']].sort_values(by='Promedio_Final'))
    
    #Filtra y muestra el detalle de los APROBADOS (ordenados por promedio).
    aprobados = df_reporte[df_reporte['Estado'] == 'APROBADO']
    if not aprobados.empty:
        print("")
        print("="*85)
        print("\nDetalle de Aprobados:")
        print(aprobados[['Nombre', 'Promedio_Final']].sort_values(by='Promedio_Final', ascending=False))
    print("")
    print("="*85)


def gestion_reportes(): #Función que maneja el sub-menú de reportes (Opción 3 del menú principal).
    try:
        #Carga el CSV antes de entrar al sub-menú de reportes.
        df = pd.read_csv(NOMBRE_CSV)
    except FileNotFoundError:
        print(f"El archivo {NOMBRE_CSV} no existe o no hay datos para generar reportes.")
        return

    #Ciclo principal del sub-menú
    while True:
        print("")
        print("*"*50,"--- GENERAR REPORTE ---","*"*50)
        print("1. Búsqueda por Nombre de Alumno")
        print("2. Calificaciones Generales (Aprobado/Reprobado)")
        print("3. Volver al Menú Principal")
        print ("*"*125)
        opcion_reporte = input("Seleccione una opción de reporte: ")

        if opcion_reporte == '1':
            buscar_alumno_por_nombre(df) #Llama a la función de búsqueda

        elif opcion_reporte == '2':
            calificaciones_generales(df) #Llama a la función de reporte general
        
        elif opcion_reporte == '3':
            break #Sale del sub-menú

        else:
            print("Opción no válida. Intente de nuevo.")


def main():    
    #Llama a la función de inicialización, asegurando la existencia del CSV.
    crear_csv_si_no_existe()
    try:
        #Ciclo principal (while) del programa.
        while True:
            #Menú principal.
            print("")
            print ("-"*165)
            print ("="*72, 'MENÚ GESTOR DE NOTAS', "="*71)
            print ("-"*165)
            print ("-"*5,"Opcion 1. Ingreso de Alumnos"," "*124,"-"*5)
            print ("-"*5,"Opcion 2. Ingreso de Notas"," "*126,"-"*5)
            print ("-"*5,"Opcion 3. Busqueda por Nombre o Calificaciones en general (Aprobado/Desaprobado)"," "*72,"-"*5)
            print ("-"*5,"Opcion 4. Editar Nota Alumno"," "*124,"-"*5) #Función de mejora
            print ("-"*5,"Opcion 5. Eliminar Alumno"," "*127,"-"*5)   #Función de mejora
            print ("-"*5,"Opcion 6. Salir del programa"," "*124,"-"*5)
            print ("-"*165)
            print("")
            
            #Solicita la opción al usuario.
            r = int(input("Ingrese una opcion (1, 2, 3 ,4, 5 o 6): "))
            print("")

            #(if/elif/else) para dirigir el flujo.
            if r==1:
                registrar_alumno()

            elif r==2:
                ingresar_notas()

            elif r == 3:
                gestion_reportes()

            elif r == 4:
                editar_notas_alumno()
            
            elif r == 5:
                eliminar_alumno()
            
            elif r == 6:
                print ("Saliendo del programa...")
                time.sleep(1.5) #Pausa
                break; #Rompe el ciclo while, terminando el programa

            else:
                print("!Ingresa una opcion válida (1, 2, 3, etc.)¡");
    
    #Manejo de error general si el usuario ingresa un valor no numérico en el menú.
    except:
        print("Error: !Ingresa una opcion valida¡")
        return 
        
main()

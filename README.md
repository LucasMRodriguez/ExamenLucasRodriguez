# 📂 GESTOR SIMPLE DE NOTAS PYTHON

## 📋 Descripción del Proyecto
Este es un **Gestor Simple de Notas** desarrollado en Python. Permite a un usuario registrar nuevos alumnos y sus asignaturas, ingresar y modificar sus calificaciones con ponderaciones, calcular promedios finales, y generar reportes de rendimiento general (aprobados/reprobados) y por alumno.

▶️ El proyecto cumple con los requisitos del Módulo de Programación Básica, incluyendo el uso de la librería **Pandas** para la persistencia, lectura y análisis básico de datos desde un archivo CSV.

## 🚀 Funcionalidades Principales
1.  **Ingreso de Alumnos:** Registra el nombre y la asignatura de un nuevo alumno, validando que no se repita el nombre.
2.  **Ingreso de Notas:** Permite añadir un conjunto de notas con sus respectivas ponderaciones, validando el rango (1.0 - 7.0) y la suma total de ponderaciones (debe ser 100%).
3.  **Reportes:**
    * **Búsqueda por Nombre:** Muestra el detalle de notas, ponderaciones, promedio final y estado (Aprobado/Reprobado) de un alumno específico.
    * **Calificaciones Generales:** Muestra el promedio general del curso y el resumen de alumnos Aprobados y Reprobados (umbral de aprobación: 4.0).
4.  **Edición de Notas:** Permite modificar una nota existente de un alumno y recalcula automáticamente su promedio final.
5.  **Eliminación:** Permite eliminar completamente un registro de alumno.

## ⚙️ Requisitos
Para ejecutar este programa, necesitas tener instalado lo siguiente:

* **Python:** Versión 3.6 o superior.
* **Librerías Adicionales:**
    ```bash
    pip install pandas
    ```

## 💻 Instrucciones para Ejecutar el Programa
1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/LucasMRodriguez/ExamenLucasRodriguez.git
    cd ruta/donde/esta/el/archivo
    ```
2.  **Instalar Librerías:**
    ```bash
    pip install pandas
    ```
3.  **Ejecutar el Archivo Principal:**
    ```bash
    python AdvancedGestorNotas.py
    ```
4.  El programa se iniciará y presentará el menú principal. Si el archivo `notas_alumnos.csv` no existe, será creado automáticamente al inicio.

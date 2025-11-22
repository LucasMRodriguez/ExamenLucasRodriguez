def main ():
    
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
                print ("!Ingreso de Alumnos¡")
                

            elif r==2:
                print ("!Ingreso de Notas¡")
                

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

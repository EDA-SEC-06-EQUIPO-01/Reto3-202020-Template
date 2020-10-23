"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys

import config
from App import controller

assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accfile = "us_accidents_small.csv"

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1 (Conocer los accidentes en una fecha)")
    print("4- Requerimento 2 (Conocer los accidentes anteriores a una fecha)")
    print("5- Requerimento 3 (Conocer los accidentes en un rango de fechas)")
    print("6- Requerimento 4 (Conocer el estado con mas accidentes)")
    print("7- Requerimento 5 (Conocer los accidentes por rango de horas)")
    print("8- Requerimento 6 (Conocer la zona geográfica mas accidentada)")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input("Seleccione una opción para continuar\n>")

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accfile)
        print("Crimenes cargados: " + str(controller.crimesSize(cont)))
        print("Altura del arbol: " + str(controller.indexHeight(cont)))
        print("Elementos en el arbol: " + str(controller.indexSize(cont)))
        print("Menor Llave: " + str(controller.minKey(cont)))
        print("Mayor Llave: " + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: \n")
        impDate = input(
            "Digite la fecha de interés; recuerde que el formato de la fecha debe ser:\n\tYYYY-MM-DD\n\t"
        )

        impDate_p1 = impDate[:-2] + (
            str(int(impDate[-2:]) + 1)
            if int(impDate[-2:]) + 1 >= 10
            else "0" + str(int(impDate[-2:]) + 1)
        )
        print(
            f"Ocurrieron {controller.R3(cont, impDate, impDate_p1)} accidentes en la fecha {impDate}"
        )

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: \n")
        finalDate = input(
            "Digite la fecha final; recuerde que el formato de la fecha debe ser:\n\tYYYY-MM-DD\n\t"
        )
        minDate = controller.minKey(cont)
        print(
            f"Ocurrieron {controller.R3(cont, minDate, finalDate)} accidentes entre la fecha {minDate} (primera fecha con registro) y la fecha {finalDate}"
        )

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: \n")
        initialDate = input(
            "Digite la fecha inicial; recuerde que el formato de la fecha debe ser:\n\tYYYY-MM-DD\n\t"
        )
        finalDate = input(
            "Digite la fecha final; recuerde que el formato de la fecha debe ser:\n\tYYYY-MM-DD\n\t"
        )
        print(
            f"Ocurrieron {controller.R3(cont, initialDate, finalDate)} accidentes entre la fecha {initialDate} y la fecha {finalDate}"
        )

    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: \n")

    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: \n")

    elif int(inputs[0]) == 8:
        print("\nRequerimiento No 6 del reto 3: \n")
        latitude = float(input("Digite la LATITUD del punto central:\n\t"))
        longitude = float(input("Digite la LONGITUD del punto central:\n\t"))
        ratio = float(input(
            "Digite el RADIO (en millas) alrededor del centro establecido;\nTenga en cuenta que aproximadamente 1° = 69.4 millas:\n\t"))
        ans = controller.R6(cont, latitude, longitude, ratio)
        print(
            f"El día en el que más se presentaron casos dentro del rango fue {ans[0]}.\nEn total ocurrieron {ans[1]} casos dentro del rango.")

    else:
        sys.exit(0)
sys.exit(0)

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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    return model.newAnalyzer()


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"), delimiter=",")
    for accident in input_file:
        model.addAccident(analyzer, accident)

    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def crimesSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.crimesSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def total_horas(analyzer, initial_hour, final_hour):
    initial_hour = datetime.datetime.strptime(initial_hour, "%H:%M:%S")
    final_hour = datetime.datetime.strptime(final_hour, "%H:%M:%S")
    return model.total_horas(analyzer, initial_hour, final_hour)


def total_accidentes(*args, **kwargs):
    """
    the mandatory arguments are analyzer and a date

    optional
    second date

    next_day
    from_begining
    """
    analyzer = args[0]

    if len(kwargs) > 0:
        if kwargs.get("next_day") == True:
            initial_date = datetime.datetime.strptime(args[1], "%Y-%m-%d")
            final_date = initial_date + datetime.timedelta(days=1)
            print(str(final_date))
        elif kwargs.get("from_begining") == True:
            initial_date = minKey(analyzer)
            final_date = datetime.datetime.strptime(args[1], "%Y-%m-%d")

    else:
        initial_date = datetime.datetime.strptime(args[1], "%Y-%m-%d")
        final_date = datetime.datetime.strptime(args[2], "%Y-%m-%d")

    return model.total_accidentes_entre_fechas(analyzer, initial_date, final_date)


def R6(analyzer, latitude, longitude, ratio):
    ratio /= 69.4
    return model.R6_AccidentesZonaGeografica(analyzer, latitude, longitude, ratio)

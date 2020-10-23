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
from datetime import date
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime

assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------


def newAnalyzer():
    analyzer = {}
    analyzer["accidents"] = lt.newList("SINGLE_LINKED", compareIds)
    analyzer["dateIndex"] = om.newMap(
        omaptype="RBT", comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo


def travel(lista: list, parameter=None):

    iter = it.newIterator(lista)

    while it.hasNext(iter):
        node = it.next(iter)

        if parameter:
            yield node[parameter]
        else:
            yield node


def addAccident(analyzer, accident):
    lt.addLast(analyzer["accidents"], accident)
    updateDateIndex(analyzer["dateIndex"], accident)
    return analyzer


def updateDateIndex(map, accident):
    occurreddate = accident["Start_Time"]
    accdate = datetime.datetime.strptime(occurreddate, "%Y-%m-%d %H:%M:%S")
    entry = om.get(map, accdate)
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accdate, datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map


def addDateIndex(datentry, accident):
    lst = datentry["lstaccidents"]
    lt.addLast(lst, accident)
    accsev = datentry["accSeverity"]
    offentry = m.get(accsev, accident["Severity"])
    if offentry is None:
        entry = newOffenseEntry(accident["Severity"], accident)
        lt.addLast(entry["lstoffenses"], accident)
        m.put(accsev, accident["Severity"], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry["lstoffenses"], accident)
    return datentry


def newDataEntry(accident):
    entry = {}
    entry["accSeverity"] = m.newMap(
        numelements=30, maptype="PROBING", comparefunction=compareOffenses
    )
    entry["lstaccidents"] = lt.newList("SINGLE_LINKED", compareDates)
    return entry


def newOffenseEntry(offensegrp, accident):
    ofentry = {}
    ofentry["offense"] = offensegrp
    ofentry["lstoffenses"] = lt.newList("SINGLE_LINKED", compareOffenses)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def crimesSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer["accidents"])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer["dateIndex"])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer["dateIndex"])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer["dateIndex"])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer["dateIndex"])


# En el R1 y R2 se utiliza el R3.


def get_range(*args, **kwargs):
    """
    first param analyzer

    the other parameters are

    initial_date
    final date
    """
    analyzer = args[0]

    initial_date, final_date = args[1:]

    return om.values(analyzer["dateIndex"], initial_date, final_date)


def total_accidentes_entre_fechas(analyzer, initial_date, final_date):
    lst = get_range(analyzer, initial_date, final_date)

    tot = 0
    for item in travel(lst, "lstaccidents"):
        tot += lt.size(item)

    return tot


def R6_AccidentesZonaGeografica(analyzer, latitude, longitude, grades):
    def inlat(lat, lat0, gr): return lat0-gr <= lat <= lat0+gr
    def inlon(lon, lon0, gr): return lon0-gr <= lon <= lon0+gr
    mp = m.newMap(comparefunction=lambda x, y: 0 if x == y['key'] else 1)
    cont = 0
    for lt_next in travel(analyzer['accidents']):
        if inlat(float(lt_next['Start_Lat']), latitude, grades) and inlon(float(lt_next['Start_Lng']), longitude, grades):
            dt = lt_next['Start_Time'][:lt_next['Start_Time'].find(' ')]
            cont += 1
            m.put(mp, dt, cont)
    maxDate = None
    mx = 0
    for i in travel(m.keySet(mp)):
        if (False if m.get(mp, i) is None else m.get(mp, i)['value'] > mx):
            mx = int(m.get(mp, i)['value'])
            maxDate = i
    return maxDate, cont

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    if id1 == id2:
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1


def compareOffenses(off1, off2):
    offense = me.getKey(off2)
    if off1 == offense:
        return 0
    elif off1 > offense:
        return 1
    else:
        return -1

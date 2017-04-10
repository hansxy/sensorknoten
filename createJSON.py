import mysql.connector as mdb
from config import *

def queryDB_station(station):
    DBconn = mdb.connect(**config)
    # This enables column access by name: row['column_name']
    #DBconn.row_factory = sqlite3.Row
    queryCurs = DBconn.cursor(dictionary=True)

    queryCurs.execute(
         'SELECT MAX(timestamp) AS timestamp, originAddr, unit,unit_name,sensor ,ANY_VALUE(id) AS id, ANY_VALUE(value) AS value '
         'FROM messwerte '
         'INNER JOIN einheiten ON messwerte.unit = einheiten.unit_id '
         'WHERE originAddr=%s GROUP BY unit '
         'ORDER BY timestamp DESC',(station,))

    row = queryCurs.fetchall()
    row_json = [ dict(rec) for rec in row ]

    DBconn.close()
    return row_json

def queryDB_station_interval(station, unit, begin, end):
    DBconn = mdb.connect(**config)
    # This enables column access by name: row['column_name']
    #DBconn.row_factory = sqlite3.Row
    queryCurs = DBconn.cursor(dictionary=True)

    queryCurs.execute(
        'SELECT timestamp, originAddr, unit,unit_name,sensor ,ANY_VALUE(id) AS id, ANY_VALUE(value) AS value '
        'FROM messwerte '
        'INNER JOIN einheiten ON messwerte.unit = einheiten.unit_id '
        'WHERE originAddr=%s AND unit=%s AND timestamp BETWEEN %s AND %s '
        'ORDER BY timestamp DESC', (station, unit,  begin, end,))

    row = queryCurs.fetchall()
    row_json = [ dict(rec) for rec in row ]

    DBconn.close()
    return row_json


def queryDB_id(id):
    DBconn = mdb.connect(**config)
    # This enables column access by name: row['column_name']
    #DBconn.row_factory = sqlite3.Row
    queryCurs = DBconn.cursor(dictionary=True)
    anwser = queryCurs.execute(
        'SELECT * '
        'FROM messwerte '
        'WHERE id=%s', (id,))
    row = queryCurs.fetchall()
    row_json = [ dict(rec) for rec in row ]
    DBconn.close()
    return row_json

def queryDBallStation():
    DBconn = mdb.connect(**config)
    # This enables column access by name: row['column_name']
    #DBconn.row_factory = sqlite3.Row
    queryCurs = DBconn.cursor(dictionary=True)
    queryCurs.execute(
        'SELECT originAddr, name , location, powerSaving '
        'FROM messwerte '
        'INNER JOIN stationen ON stationen.station_id = messwerte.originAddr '
        'GROUP BY originAddr')
    row = queryCurs.fetchall()
    row_json = [ dict(rec) for rec in row ]
    DBconn.close()
    return row_json

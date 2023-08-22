import datetime

import mysql.connector

def AgregarAlerta(alerta):
    try:
        myconn = mysql.connector.connect(host="192.168.0.29", user="PythonClient", passwd="nico386",
                                         database="TestDatabase")
        cursor = myconn.cursor()

        sql = "INSERT INTO Alertas (`Grupo`, `Simbolo`, `Direccion`, `PrecioEntrada`, `Hora`, `Estado`) VALUES ('{}'," \
              "'{}','{}',{},'{}',{})".format(alerta['GRUPO'], alerta['SIMBOLO'], alerta['DIRECCION'],
                                             alerta['PRECIOS']['ENTRADA'], alerta['HORA'], 0)
        cursor.execute(sql)
        myconn.commit()
        id_alerta = cursor.lastrowid

        sql = "INSERT INTO Precios (IdAlerta,Tipo,Precio) VALUES ({},'{}',{})".format(id_alerta, 'SL', alerta['PRECIOS']['SL'])
        cursor.execute(sql)
        myconn.commit()

        sql = "INSERT INTO Precios (IdAlerta,Tipo,Precio) VALUES ({},'{}',{})"
        for tp in alerta['PRECIOS']['TP']:
            cursor.execute(sql.format(id_alerta, 'TP', tp))
            myconn.commit()
        print("ALERTA AGREGADA ", alerta)
        cursor.close()
        myconn.close()
    except Exception as e:
        print(e)

def GetAlertasAbiertas():
    # Crear una conexión a la base de datos
    try:
        myconn = mysql.connector.connect(host="192.168.0.29", user="PythonClient", passwd="nico386",
                                         database="TestDatabase")
        cursor = myconn.cursor()

        # Ejecutar la consulta
        query = "SELECT * FROM Alertas WHERE ESTADO = 0"
        cursor.execute(query)

        # Obtener los datos y almacenarlos en un diccionario
        lista_alertas = []
        for row in cursor.fetchall():
            alerta = {}
            alerta['ID'] = row[0]
            alerta['SIMBOLO'] = row[1]
            alerta['DIRECCION'] = row[2]
            alerta['PRECIOS'] ={'ENTRADA': row[3]}
            alerta['HORA'] =datetime.datetime.fromtimestamp(int(row[4]))
            alerta['ESTADO'] = row[5]
            alerta['GRUPO'] = row[6]
            lista_alertas.append(alerta)


        for alerta in lista_alertas:
            query = f"SELECT * FROM Precios WHERE IdAlerta = {alerta['ID']}"
            cursor.execute(query)
            tp = []
            for row in cursor.fetchall():
                if row[1] == 'SL':
                    alerta['PRECIOS']['SL'] = float(row[2])
                else:
                    tp.append(float(row[2]))
            alerta['PRECIOS']['TP'] = tp
        # Cerrar el cursor y la conexión
        cursor.close()
        myconn.close()
        #lista_ordenada = sorted(lista_alertas, key=lambda x: x["SIMBOLO"])
        return lista_alertas


    except mysql.connector.Error as err:
        print(f"Error al conectar o ejecutar la consulta: {err}")
        return None

def SetAlertaInvalida(alerta):
    try:
        myconn = mysql.connector.connect(host="192.168.0.29", user="PythonClient", passwd="nico386",
                                         database="TestDatabase")
        cursor = myconn.cursor()

        sql = f"UPDATE Alertas SET Estado = -2 WHERE IdAlerta = {alerta['ID']}"
        cursor.execute(sql)
        myconn.commit()

        cursor.execute(sql)
        myconn.commit()
        cursor.close()
        myconn.close()
    except Exception as e:
        print(e)

def SetEstadoAlerta(alerta):
    try:
        myconn = mysql.connector.connect(host="SERVER IP", user="USR", passwd="PASS",
                                         database="TestDatabase")
        cursor = myconn.cursor()

        sql = f"UPDATE Alertas SET Estado = {alerta['ESTADO']} WHERE IdAlerta = {alerta['ID']}"
        cursor.execute(sql)
        myconn.commit()

        cursor.execute(sql)
        myconn.commit()
        cursor.close()
        myconn.close()
    except Exception as e:
        print(e)

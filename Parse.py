from datetime import datetime

PORCENTAJE_SL = 1
PORCENTAJE_TP_01 = 0.5
PORCENTAJE_TP_02 = 1
PORCENTAJE_TP_03 = 1.5


def calcularSLyTP(precio, direccion):
    if direccion == "SHORT":
        precio_sl = precio + (float(precio) * (PORCENTAJE_SL / 100))
        precio_tp_01 = precio - (float(precio) * (PORCENTAJE_TP_01 / 100))
        precio_tp_02 = precio - (float(precio) * (PORCENTAJE_TP_02 / 100))
        precio_tp_03 = precio - (float(precio) * (PORCENTAJE_TP_03 / 100))

    if direccion == "LONG":
        precio_sl = precio - (float(precio) * (PORCENTAJE_SL / 100))
        precio_tp_01 = precio + (float(precio) * (PORCENTAJE_TP_01 / 100))
        precio_tp_02 = precio + (float(precio) * (PORCENTAJE_TP_02 / 100))
        precio_tp_03 = precio + (float(precio) * (PORCENTAJE_TP_03 / 100))

    return {'ENTRADA': precio, 'SL': precio_sl, 'TP': [precio_tp_01, precio_tp_02, precio_tp_03]}


def message_to_dict(grupo, mensaje):

    if grupo == 'Trading BitBot - Picker':
        alerta = {}
        m = mensaje.split()
        if m[0] == '🟢':
            alerta['DIRECCION'] = 'LONG'
        elif m[0] == '🔴':
            alerta['DIRECCION'] = 'SHORT'
        alerta['SIMBOLO'] = m[1]
        alerta['GRUPO'] = grupo

        alerta['PRECIOS'] = calcularSLyTP(float(m[4]),alerta['DIRECCION'])

        alerta['HORA'] = int(datetime.utcnow().timestamp())
        return alerta


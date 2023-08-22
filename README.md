# TelegramSQL Pt 1
This is the first part of a bigger project using trading alerts from telegram

In this series of scripts we will:

- Get all alerts messages from diferent telegram groups
- Parse the messages into a python dictionary
- Save that dictionary to a MySql Server

The telegram message has this format:

![image](https://github.com/NicoGiovi/TelegramSQL/assets/16262582/75eb5faa-b70a-4645-8191-fd1a699329c8)

To Store it we will need a only 2 tables:

Alertas
  IdAlertas
  Simbolo
  Direccion
  PrecioEntrada
  Hora
  Estado
  Grupo

Precios
  IdAlerta
  Tipo
  Precio

The general idea is for the script system to capture alerts from Telegram groups and store them. Later, these alerts are processed by assigning them multiple arbitrary take profit levels and a stop loss. Then, based on the time the alert was received, the candles are fetched from Binance Futures to assign them a state:
0 if the alert has not been processed yet.
-2 if the candles couldn't be fetched for that symbol.
-1 if the alert reached a stop loss.
And 1, 2, 3 if the alert reached the different take profits (TPs).


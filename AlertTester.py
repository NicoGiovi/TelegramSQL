import asyncio
import datetime

from binance import AsyncClient

from Persistencia import GetAlertasAbiertas, SetAlertaInvalida, SetEstadoAlerta


class GetAllBinanceData:
    def __init__(self, workers_num: int = 10):
        self.workers_num: int = workers_num
        self.task_q: asyncio.Queue = asyncio.Queue(maxsize=10)

    async def get_symbols_from_somewhere(self):
        """Get symbols and distribute them among workers"""
        # imagine the symbols are from some file

        symbols = GetAlertasAbiertas()
        for i in symbols:
            await self.task_q.put(i)

        for i in range(self.workers_num):
            await self.task_q.put(None)

    async def get_historical_klines(self, client: AsyncClient):

        while True:
            alerta = await self.task_q.get()
            if alerta is None:
                break
            try:
                klines = await client.get_historical_klines(
                    symbol=alerta['SIMBOLO'],
                    interval=AsyncClient.KLINE_INTERVAL_5MINUTE,
                    start_str=str(alerta['HORA']),
                    end_str=str(alerta['HORA'] + datetime.timedelta(hours=24))
                )
                # 0 = Timestamp, 1 = Open, 2 = Hi, 3 = Low, 4 = Close
                for k in klines:
                    if alerta['DIRECCION'] == 'SHORT':
                        if alerta['ESTADO'] == 0 and float(k[2]) >= float(alerta['PRECIOS']['SL']):
                            alerta['ESTADO'] = -1
                            break

                        if alerta['ESTADO'] == 0 and float(k[3]) <= float(alerta['PRECIOS']['TP'][0]):
                            alerta['ESTADO'] = 1
                        if alerta['ESTADO'] == 1 and float(k[3]) <= float(alerta['PRECIOS']['TP'][1]):
                            alerta['ESTADO'] = 2
                        if alerta['ESTADO'] == 2 and float(k[3]) <= float(alerta['PRECIOS']['TP'][2]):
                            alerta['ESTADO'] = 3

                        if alerta['ESTADO'] > 0 and float(k[2]) >= float(alerta['PRECIOS']['SL']):
                            break

                    if alerta['DIRECCION'] == 'LONG':
                        if alerta['ESTADO'] == 0 and float(k[2]) <= float(alerta['PRECIOS']['SL']):
                            alerta['ESTADO'] = -1
                            break

                        if alerta['ESTADO'] == 0 and float(k[3]) >= float(alerta['PRECIOS']['TP'][0]):
                            alerta['ESTADO'] = 1
                        if alerta['ESTADO'] == 1 and float(k[3]) >= float(alerta['PRECIOS']['TP'][1]):
                            alerta['ESTADO'] = 2
                        if alerta['ESTADO'] == 2 and float(k[3]) >= float(alerta['PRECIOS']['TP'][2]):
                            alerta['ESTADO'] = 3

                        if alerta['ESTADO'] > 0 and float(k[2]) <= float(alerta['PRECIOS']['SL']):
                            break
                print(alerta['SIMBOLO'],alerta['ESTADO'])
                SetEstadoAlerta(alerta)
            except Exception as e:
                print(e)
                if str(e) == "APIError(code=-1121): Invalid symbol.":
                    SetAlertaInvalida(alerta)

    async def amain(self) -> None:
        while True:
            """Main async wrapper fucntion"""
            try:
                client = await AsyncClient.create()
                await asyncio.gather(
                    self.get_symbols_from_somewhere(),
                    *[self.get_historical_klines(client) for _ in range(self.workers_num)])
                await client.close_connection()
            except Exception as e:
                print(str(e).split())
            await asyncio.sleep(3600)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData().amain())

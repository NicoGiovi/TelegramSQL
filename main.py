from telethon.sync import TelegramClient, events
from Parse import message_to_dict
from Persistencia import AgregarAlerta

api_id = 13260429
api_hash = 'b51cb23b660dbe1d48b9aca63e0a9be2'
usr_name = "Nico Giovi"

print("*SERVIDOR DE TELEGRAM INICIADO*")

with TelegramClient(usr_name, api_id, api_hash) as client:
    @client.on(events.NewMessage())
    async def handler(event):

        chat_from = event.chat if event.chat else (await event.get_chat())
        try:
            if not event.message.is_reply:
                alerta = message_to_dict(chat_from.title, event.text)
                if alerta is not None:
                    AgregarAlerta(alerta)
        except Exception as e:
            print(e)

    client.run_until_disconnected()

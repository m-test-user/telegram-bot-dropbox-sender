import datetime
import os
import shutil
from tempfile import TemporaryFile

import dropbox
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
DBX = os.getenv('DROPBOX_TOKEN')

dbx = dropbox.Dropbox(DBX)
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
tmp_dir = 'tmp'
 

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Бот отправляющий сообщеия в DropBox, активирован')
    raise events.StopPropagation


@bot.on(events.NewMessage)
async def save_msg(event):
    
    time_stamp = str(datetime.datetime.today())
    output_tmp_name = f'tmp{time_stamp.replace(":", "-")}'
    
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)

    with open(f'./tmp/{output_tmp_name}', 'w', encoding='utf8') as tmp_file:
        tmp_file.write(f'#inbox #telegram\n---\n\n{event.text}')

    send_file_dbx()
    shutil.rmtree(tmp_dir)

    await event.respond('Отправлено')
    raise events.StopPropagation


def send_file_dbx():
    print('+')
    list_files = os.listdir(tmp_dir)

    for index in list_files:
        with open(f'./tmp/{index}','rb') as file:
            file_name = index.replace('tmp', '')
            dbx.files_upload(file.read(), f'/{file_name}.md')
            print('done')


def main():
    print('run')
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()

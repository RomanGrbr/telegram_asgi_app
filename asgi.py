import asyncio
import logging
import os
import sys

import uvicorn
from pyngrok import ngrok

from core.application import ASGIApplication, JSONResponse
from core.bot import Bot
from core.updater import Update
from core.settings import HOST, NGROK_TOKEN, PORT
from core.handlers.dispatcher import setup_dispatcher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{BASE_DIR}/output.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

app = ASGIApplication()
bot = Bot()


@app.post('/webhook')
async def init(request):
    update = Update(request=request, bot=bot)
    await setup_dispatcher(update)
    await update.run_handlers()

    # await update.reply_text(text=f'Hello, {name}', chat_id=chat_id)
    return JSONResponse(content={'status': 'ok'}, code=200)


def run_server(host, port):
    uvicorn.run(
        app='asgi:app',
        host=host,
        port=port,
        log_level='info',
        reload=True)


async def main():
    # ngrok.set_auth_token(NGROK_TOKEN)
    # public_url = ngrok.connect(PORT, bind_tls=True).public_url
    # print(f'SET PUBLIC URL: {public_url}/webhook')
    # await bot.set_webhook(f'{public_url}/webhook')
    run_server(HOST, PORT)

if __name__ == '__main__':
    asyncio.run(main())

import logging
import os
import sys

from core.application import ASGIApplication, JSONResponse
from core.bot import BotBilder
from core.updater import Update
from core.settings import BOT_TOKEN
from handlers.dispatcher import setup_dispatcher

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
app_bot = BotBilder(BOT_TOKEN)


@app.post('/webhook')
async def init(request):
    update = Update(request=request, bot=app_bot.bot)
    await app_bot.updater(update)
    return JSONResponse(content={'status': 'ok'}, code=200)

setup_dispatcher(app_bot)


# def run_server(host, port):
#     uvicorn.run(
#         app='asgi:app',
#         host=host,
#         port=port,
#         log_level='info',
#         reload=True)


if __name__ == '__main__':
    # ngrok.set_auth_token(NGROK_TOKEN)
    # public_url = ngrok.connect(PORT, bind_tls=True).public_url
    # print(f'SET PUBLIC URL: {public_url}/webhook')
    # app_bot.set_webhook(f'{public_url}/webhook')
    # run_server(HOST, PORT)

    os.system('uvicorn asgi:app --reload')

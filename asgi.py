import asyncio
import logging
import os
import sys

import uvicorn
from pyngrok import ngrok

from core.asgi import ASGIApplication, JSONResponse
from core.settings import PORT, HOST, NGROK_TOKEN

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


@app.post('/webhook')
async def init(bot):
    print(bot.message)
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
    # await app.bot.set_webhook(f'{public_url}/webhook')
    run_server(HOST, PORT)

if __name__ == '__main__':
    asyncio.run(main())

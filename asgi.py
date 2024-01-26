import logging
import os
import sys

import uvicorn

from core.asgi import ASGIApplication

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = ASGIApplication()


def run_server(host, port):
    uvicorn.run(
        app='asgi:app',
        host=host,
        port=port,
        log_level='info',
        reload=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{BASE_DIR}/output.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    run_server('127.0.0.1', int(sys.argv[1]))

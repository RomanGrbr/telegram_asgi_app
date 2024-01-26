# asgi_app

Чтобы сделать пакетным менеджером poetry в уже имеющемся проекте
poetry init

Чтобы установить зависимости проекта
poetry install

Чтобы обновить версии зависимостей
poetry update

Чтобы добавить новую библиотеку
poetry add <name>


Запустить сервер
python3 asgi.py 8000

или так
uvicorn asgi:app 8000

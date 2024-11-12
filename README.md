## Простое приложение на FastAPI для получения информации о процессоре

Запуск: uvicorn app:app --workers 1 --host 0.0.0.0 --port 1234

Роуты:
1. Cинхронный - http://0.0.0.0:1234/sync_info
2. Асинхронный - http://0.0.0.0:1234/async_info
3. Swagger - http://0.0.0.0:1234/docs

pip install -r requirements.txt
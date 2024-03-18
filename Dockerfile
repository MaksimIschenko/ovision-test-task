FROM python

# Создаем рабочую директорию для приложения
RUN mkdir /fastapi_app
WORKDIR /fastapi_app

# Копируем файл зависимостей
COPY requirements.txt ./

# Устанавливаем необходимые системные библиотеки
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install -r requirements.txt

# Копируем оставшиеся файлы проекта
COPY . .

RUN chmod a+x docker/*.sh

#RUN alembic upgrade head

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

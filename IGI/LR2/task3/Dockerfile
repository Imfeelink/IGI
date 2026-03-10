# 1. Выбираем базовый образ (уже готовая ОС с установленным Python)
FROM python:3.9-slim

# 2. Устанавливаем git, чтобы скачать библиотеку из GitHub
RUN apt-get update && apt-get install -y git

# 3. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 4. Скачиваем библиотеку напрямую из репозитория в текущую папку
RUN git clone https://github.com/smartiqaorg/geometric_lib.git .

# 5. Копируем наш файл main.py с компьютера в контейнер (в папку /app)
COPY main.py .

# 6. Указываем команду, которая выполнится при запуске контейнера
CMD ["python", "main.py"]
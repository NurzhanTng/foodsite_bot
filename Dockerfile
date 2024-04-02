# Используйте официальный образ Python в качестве базового образа
FROM python:3.11-slim

# Установите рабочую директорию в контейнере
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install  -r requirements.txt
# Скопируйте файлы вашего проекта в контейнер
COPY . .

# Установите зависимости из файла requirements.txt

# Определите команду для запуска вашего бота
CMD ["python3", "main.py"]


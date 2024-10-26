FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN echo "source activate my_env" > ~/.bashrc

ENV PATH /opt/conda/envs/my_env/bin:$PATH

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование кода
COPY . .

CMD ["python", "app.py"]

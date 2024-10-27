FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN echo "source activate my_env" > ~/.bashrc

ENV PATH /opt/conda/envs/my_env/bin:$PATH

# Установка зависимостей
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libgl1 \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

# Копирование кода
COPY . .

CMD ["python", "app.py"]

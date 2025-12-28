FROM python:3.11-slim

# Устанавливаем зависимости для Pygame + виртуальный дисплей
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libx11-dev \
    libxcursor-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxi-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем игру
COPY main.py .

# Создаем скрипт запуска с виртуальным дисплеем
RUN echo '#!/bin/bash\n\
Xvfb :1 -screen 0 1024x768x24 & \n\
export DISPLAY=:1 \n\
exec python main.py' > /app/run.sh \
    && chmod +x /app/run.sh

# Запуск через виртуальный дисплей
CMD ["/app/run.sh"]

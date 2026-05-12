FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости из файла
RUN pip3 install --no-cache-dir -r requirements.txt

# Затем копируем сам скрипт
COPY script.py .

# Запускаем скрипт с правильным названием
CMD ["python3", "script.py"]
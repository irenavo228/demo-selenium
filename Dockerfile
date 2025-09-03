FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    wget gnupg curl ca-certificates fonts-liberation \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdbus-1-3 libdrm2 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libgtk-3-0 libnspr4 libnss3 \
    libxss1 libxtst6 lsb-release xdg-utils \
    unixodbc-dev docker.io bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /app/venv

COPY requirements.txt /app/

RUN /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install -r requirements.txt \
    && /app/venv/bin/python -m playwright install

COPY . /app

ENV PATH="/app/venv/bin:$PATH"

CMD ["pytest", "/app/tests"]
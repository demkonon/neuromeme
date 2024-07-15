# Базовый образ
FROM ghcr.io/berriai/litellm:main-latest

# Установка рабочей директории
WORKDIR /app

# Копирование файла конфигурации в образ
COPY config.yaml /app/config.yaml

CMD ["--port", "4000"]
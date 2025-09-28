FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    opencv-python opencv-contrib-python Pillow fastapi uvicorn

WORKDIR /app
COPY . /app

# Запускаем API
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

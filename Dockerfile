FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    opencv-contrib-python-headless Pillow fastapi uvicorn python-multipart

WORKDIR /app
COPY . /app

CMD ["uvicorn", "script:app", "--host", "0.0.0.0", "--port", "8060"]

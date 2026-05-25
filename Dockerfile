FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y \
    ffmpeg \
    gcc \
    python3-dev

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libopus0 tesseract-ocr && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home guardbot && chown -R guardbot /app
USER guardbot
HEALTHCHECK --interval=60s --timeout=5s --start-period=60s CMD python -c "import sys,time;sys.exit(0 if time.time()-int(open('data/heartbeat').read())<120 else 1)"
CMD ["python", "main.py"]

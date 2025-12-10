FROM python:3.12-slim


RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["python", "bot.py"]

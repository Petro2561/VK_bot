FROM python:3.10.0

COPY requirements.txt /app/requirements.txt
COPY bot_vk /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
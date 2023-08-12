
FROM python:3.11


WORKDIR /app

COPY Bot.py /app/


CMD ["python", "bot.py"]

FROM jfloff/alpine-python:3.6-slim

COPY app /app
WORKDIR /app

RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=main.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

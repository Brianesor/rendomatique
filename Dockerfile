FROM python:3.12.0-slim-bullseye
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=rendomatique.py
CMD gunicorn --bind 0.0.0.0:5000 rendomatique:app
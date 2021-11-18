# syntax=docker/dockerfile:1

FROM python:3.9-slim


WORKDIR /apache_kafka

COPY requirements.txt requirements.txt
RUN apt-get update -y && apt-get install -y gcc && apt-get install -y librdkafka-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]
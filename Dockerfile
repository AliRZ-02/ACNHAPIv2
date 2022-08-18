# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-slim

LABEL Maintainer="Ali Raza Zaidi"

COPY . /app/ACNHAPIv2

WORKDIR /app/ACNHAPIv2

USER root

RUN apt update

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
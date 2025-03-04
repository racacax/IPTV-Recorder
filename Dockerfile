# ===== builder step =====
FROM python:3.12-bullseye AS builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBCONF_NOWARNINGS=yes
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

# System layer
RUN apt update && apt install -y wget ffmpeg
# Python dependencies layer
COPY requirements.txt requirements.txt /app/
COPY requirements-dev.txt requirements.txt /app/
RUN pwd && ls -la && pip install --upgrade pip && pip install -r requirements.txt
RUN chmod 777 .

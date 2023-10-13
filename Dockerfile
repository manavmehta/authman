FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 8000
FROM python:3.11.6
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 8000
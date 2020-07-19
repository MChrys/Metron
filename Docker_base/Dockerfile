FROM python:3.8.0-alpine
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev 
RUN apk add --no-cache bash
RUN pip install --upgrade pip
# install dependencies
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt

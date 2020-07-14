FROM python:3.7
COPY . /app
ENV APP_SETTINGS="config.DevelopmentConfig"
ENV DATABASE_URL="postgresql:///root:password@0.0.0.0:5432/metron_database"
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
#CMD ["app.py"]
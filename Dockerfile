FROM base-app:latest
COPY . /app
WORKDIR /app
#ENV APP_SETTINGS="config.DevelopmentConfig"
#ENV DATABASE_URL="postgresql+psycopg2://metron:password@0.0.0.0:5432/metron_database"
EXPOSE 5000
#RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
ARG file_app
ENV file_app=${file_app}
#CMD [ "python migrate.py db init", "python migrate.py db migrate","python migrate.py db upgrade","python app.py"]
CMD python $file_app 
FROM base-app:latest
COPY . /app
WORKDIR /app

EXPOSE 5000

ARG file_app
ENV file_app=${file_app}
ENV FLASK_APP=${file_app}

CMD python $file_app 
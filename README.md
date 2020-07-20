# Metron

## first mount the base container :
  docker build -t base-app:latest ./Docker_base

## then mount the docker-compose and run it :
  docker-compose build <br>
  docker-compose up
  
## open an other terminal and run a bash from the web app container :
  docker-compose run web bash
 
## inside the bash you can now run tox command :
  tox -e pytest <br>
  tox -e lint 

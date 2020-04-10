############ Base ############
FROM python:3.7 as base

RUN apt-get -y update \
    && apt-get -y upgrade \
    && mkdir /app

WORKDIR /app
###############################


############ Build ############
FROM base as build

ENV PYTHONUNBUFFERED 1

COPY Pipfile /app
COPY Pipfile.lock /app

RUN pip install pipenv \
    && pipenv install --system --deploy
###############################


############ production ############
FROM build as production

COPY . /app

EXPOSE 80

CMD ["python", "app.py"]
###############################

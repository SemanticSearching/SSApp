FROM continuumio/miniconda3
LABEL MAINTAINER="Mykhailo Nenych"
WORKDIR /opt/app
COPY ./ ./
RUN conda env update --file py38.yml
SHELL ["conda", "run", "-n", "py38", "/bin/bash", "-c"]
RUN cd /opt/app/app/parser_engine/pySBD && pip install -e ./
# PostGrel
ARG DB_USER
ARG DB_PASS
ARG DB_HOST
ARG DB_NAME
# UI
ARG LOGIN_USER
ARG LOGIN_PASSWORD
# AWS
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
#ARG AWS_DEFAULT_REGION

#
RUN conda env config vars set DB_USER=$DB_USER
RUN conda env config vars set DB_PASS=$DB_PASS
RUN conda env config vars set DB_HOST=$DB_HOST
RUN conda env config vars set DB_NAME=$DB_NAME
RUN conda env config vars set LOGIN_USER=$LOGIN_USER
RUN conda env config vars set LOGIN_PASSWORD=$LOGIN_PASSWORD
RUN conda env config vars set AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
RUN conda env config vars set AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
#RUN conda env config vars set AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV FLASK_APP=ssapp.py
ENV FLASK_ENV=development
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "py38", "flask","run", "--host=0.0.0.0"]

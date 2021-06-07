FROM continuumio/miniconda3
LABEL MAINTAINER="Mykhailo Nenych"
WORKDIR /opt/app
COPY ./ ./
RUN conda env update --file py38.yml
SHELL ["conda", "run", "-n", "py38", "/bin/bash", "-c"]
RUN cd /opt/app/app/parser_engine/pySBD && pip install -e ./
RUN conda env config vars set DOMAIN=http://semanticsearch.site
RUN conda env config vars set USERNAME=parc
RUN conda env config vars set PASSWORD=sss
ENV FLASK_APP=ssapp.py
ENV FLASK_ENV=development
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "py38", "flask","run", "--host=0.0.0.0"]

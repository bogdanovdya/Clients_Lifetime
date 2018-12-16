FROM python:3.6-alpine

RUN adduser -D root

WORKDIR /home/cliens_lifetime

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY bitrix24 bitrix24
COPY cert cert
COPY model model
COPY templates templates

COPY app.py app_settings.py botApplication.py indexApplication.py installApplication.py main.py models.py test.py view.py ./

ENV FLASK_APP main.py

RUN chown -R main:main ./

USER root

EXPOSE 443

ENTRYPOINT ["./boot.sh"]
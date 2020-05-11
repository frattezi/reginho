FROM python:2.7-alpine


RUN pip install redis elasticsearch elasticsearch_dsl

COPY ./ /app/

WORKDIR /app

CMD [ "python", "subscriber.py" ]
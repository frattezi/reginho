FROM python:2.7-alpine


RUN pip install redis

COPY ./ /app/

WORKDIR /app

CMD [ "python", "publisher.py" ]
FROM python:3.8

WORKDIR /app

RUN pip3 install rbwriter
RUN chmod 777 /app

RUN rbwriter docker-init

EXPOSE 8000

CMD ["rbwriter start"]

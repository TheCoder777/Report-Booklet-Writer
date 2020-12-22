FROM python:3.8

WORKDIR /app

RUN pip3 install rbwriter
RUN chmod 777 /app

RUN rbwriter start

EXPOSE 80

CMD ["rbwriter start"]

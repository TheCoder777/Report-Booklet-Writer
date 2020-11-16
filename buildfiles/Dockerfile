FROM python:3.8

WORKDIR /app

RUN apt-get update
RUN apt-get install -qq python3 python3-pip
RUN pip3 install rbwriter
RUN mkdir files
RUN chmod 777 files/

ENTRYPOINT ["./files/buildfiles/init.sh"]
EXPOSE 8000
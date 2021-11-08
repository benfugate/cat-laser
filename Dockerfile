FROM arm32v7/php:latest

COPY requirements.txt .
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-dev python3-pip python3-numpy
RUN pip3 install -r requirements.txt

COPY www/ /var/www/html/
COPY src/ /laser/src/
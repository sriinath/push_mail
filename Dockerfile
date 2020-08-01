FROM ubuntu:latest

LABEL maintainer = "sriinathk@gmail.com"

RUN apt-get update && apt-get install -y python3-pip && apt-get install -y git
RUN git clone https://github.com/sriinath/push_mail.git
WORKDIR /push_mail
RUN pip3 install -r requirements.txt

CMD uwsgi --ini uwsgi.ini

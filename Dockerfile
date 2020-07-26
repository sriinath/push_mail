# FROM nginx:latest
  
# COPY nginx.conf /etc/nginx/sites-available/

# RUN mkdir /etc/nginx/sites-enabled/
# RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/
# RUN /etc/init.d/nginx restart

FROM ubuntu:latest

MAINTAINER Srinath K "sriinathk@gmail.com"

RUN apt-get update && apt-get install -y python3-pip && apt-get install -y git
RUN git clone https://github.com/sriinath/push_mail.git
WORKDIR /push_mail
RUN pip3 install -r requirements.txt && pip3 install requests

CMD uwsgi --ini uwsgi.ini
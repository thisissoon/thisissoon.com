FROM ubuntu:14.04
RUN apt-get update
RUN apt-get install -y python python-pip python-dev libpq-dev git
RUN git clone https://github.com/thisissoon/thisissoon.com.git soon
WORKDIR /soon
RUN make develop
EXPOSE 5000
RUN manage.py db upgrade
CMD ["manage.py", "runserver"]

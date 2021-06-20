FROM python:3.6.1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip install -Iv selenium==3.141.0
RUN apt-get update
RUN apt-get install mysql-client-5.5 -y
RUN apt-get install gettext -y

# create unprivileged user
RUN adduser --disabled-password --gecos '' shhh

ADD ./main.py /main.py
EXPOSE 8000

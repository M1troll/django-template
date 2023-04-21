FROM python:3.11

RUN mkdir /code
WORKDIR /code

ADD requirements/local_build.txt /code/
RUN pip install -r local_build.txt
ADD . /code/
RUN inv project.install-requirements

EXPOSE 8000

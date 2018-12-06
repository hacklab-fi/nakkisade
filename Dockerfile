FROM python:3
RUN apt update
RUN apt -y install gettext
ENV PYTHONUNBUFFERED 1
RUN mkdir /code 
WORKDIR /code
ADD requirements.txt /code/ 
RUN pip install -r requirements.txt 
ADD . /code/
ENTRYPOINT ["/code/entrypoint.sh"]

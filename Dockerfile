 FROM python:3.6
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD config/requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD ./src/ /code/
 ADD config/gunicorn /code/
 RUN ls -l
 RUN pwd
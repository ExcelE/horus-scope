FROM python:3.6.6
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#RUN python label_image.py --image temp.jpg
# CMD [ "gunicorn", "-k" ,"flask_sockets.worker", "app:app", "--bind", "0.0.0.0:5000"]
CMD [ "uwsgi", "--ini", "app.ini" ]

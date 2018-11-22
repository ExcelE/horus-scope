FROM python:3.6.6
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./classifier/ /classifier/
RUN ls -la /classifier/
COPY . .
RUN ls -la
RUN python label_image.py --image temp.jpg
CMD [ "python", "app.py" ]

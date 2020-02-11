FROM python:3
WORKDIR /usr/src/app
COPY ./serverlora.py ./
COPY ./config.json ./
RUN pip install python-time
RUN pip install paho.mqtt
RUN pip install jsonlib-python3
RUN pip install influxdb
CMD [ "python", "-u", "./serverlora.py" ]


FROM python:3
RUN pip3 install paho-mqtt python-etcd &&\
    pip3 install python-decouple
COPY . /app
CMD python3 /app/main.py

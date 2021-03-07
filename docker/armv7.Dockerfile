FROM balenalib/raspberry-pi2-debian-python:3.8

RUN [ "cross-build-start" ]

RUN pip install phue

WORKDIR /code
COPY . .

CMD [ "python", "hue-poll.py" ]

RUN [ "cross-build-end" ]

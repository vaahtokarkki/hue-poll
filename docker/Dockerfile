FROM python:3.8-alpine

RUN pip install phue

WORKDIR /code
COPY . .

CMD ["python", "hue-poll.py"]
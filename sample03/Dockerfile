FROM python:3-alpine

ADD . /app
WORKDIR /app
RUN pip install requests

CMD ["python", "server.py"]
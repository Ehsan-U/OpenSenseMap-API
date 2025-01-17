FROM python:3.10-alpine3.21

WORKDIR /src

COPY . .

CMD ["python3","app.py"]



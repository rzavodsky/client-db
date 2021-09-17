FROM python:3

WORKDIR /code

RUN apt install gcc libpq-dev
COPY requirements.txt /code/
RUN pip install -r requirements.txt

CMD ["python", "app.py"]

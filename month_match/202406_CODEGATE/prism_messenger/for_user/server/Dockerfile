FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN useradd -m -u 1000 user

USER user

COPY ./main.py /app/main.py

CMD [ "python", "-u", "/app/main.py" ]

FROM python:3.5
MAINTAINER Marco Ceppi <marco@thesilphroad.com>

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]

FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

WORKDIR /quizapp-docker

COPY . .

RUN pip3 install -r requirements.txt

RUN python manage.py collectstatic --noinput





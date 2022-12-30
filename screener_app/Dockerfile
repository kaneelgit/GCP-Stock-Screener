FROM python:3.8.10

ENV PYTHONBUFFERED True

ENV APP_HOME /dummy_app

WORKDIR ${APP_HOME}

COPY . ./

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
FROM python:3.5-alpine

COPY . /rcblog

RUN pip3 install -r /rcblog/requirements.txt

EXPOSE 8000

WORKDIR /rcblog

CMD ["gunicorn", "-b", "0.0.0.0:8000", "rcblog:app"]

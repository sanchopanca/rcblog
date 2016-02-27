FROM python:3.5-alpine

COPY . /rcblog

RUN pip3 install -r /rcblog/requirements.txt

EXPOSE 5000

WORKDIR /rcblog

CMD ["python3", "run.py"]

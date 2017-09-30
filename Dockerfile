FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

# install uwsgi
RUN pip install uwsgi
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uwsgi", "--http-socket", "0.0.0.0:5000", "--wsgi-file", "run.py", "--callable", "app"]
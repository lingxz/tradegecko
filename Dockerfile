FROM lbracken/flask-uwsgi

EXPOSE 5000

CMD ["uwsgi", "--http-socket", "0.0.0.0:5000", "--wsgi-file", "run.py", "--callable", "app"]
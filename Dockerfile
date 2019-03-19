FROM edemskiy/ubuntu-ml-server

WORKDIR /app
COPY . /app

ENV FLASK_APP=main.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

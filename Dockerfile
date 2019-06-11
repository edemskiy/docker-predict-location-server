FROM edemskiy/ubuntu-ml-server

WORKDIR /app
COPY . /app

RUN pip3 install tensorflow==1.5

ENV FLASK_APP=main.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

FROM ubuntu:20.04
RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD [ "python3", "./app.py" ]
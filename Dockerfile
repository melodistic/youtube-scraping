FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update
RUN apt install -y python3-pip
RUN apt install -y ffmpeg

RUN mkdir /app
WORKDIR /app
COPY * /app/

RUN pip3 install -r requirements.txt

RUN python3 generate_json.py
CMD ["python3", "download.py"]
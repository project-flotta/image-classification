FROM python:3.10-slim-bullseye

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip 

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3" , "main.py"]
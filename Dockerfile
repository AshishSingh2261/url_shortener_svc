FROM python:3.9.13

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN apt-get update && apt-get install -y zbar-tools

WORKDIR /app

COPY src /app/src
COPY runserver.sh /app/runserver.sh
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
EXPOSE 5000

CMD ["bash", "runserver.sh"]
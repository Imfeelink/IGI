FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app

RUN git clone https://github.com/smartiqaorg/geometric_lib.git .

COPY main.py .

CMD ["python", "main.py"]
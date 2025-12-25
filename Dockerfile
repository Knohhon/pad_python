FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd 

COPY . .

RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY StationService.py .

RUN pip install -r requirements.txt

EXPOSE 5003

CMD python3 StationService.py

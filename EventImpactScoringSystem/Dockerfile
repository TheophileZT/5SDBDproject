FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY EventImpactScoringSystem.py .

RUN pip install -r requirements.txt

EXPOSE 5002

CMD python3 EventImpactScoringSystem.py

FROM python:3.12

WORKDIR /EventImpactScoringSystem

COPY ../GitRepos/Projet5SDBD/EventImpactScoringSystem .

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["python3", "EventImpactScoringSystem.py", ]
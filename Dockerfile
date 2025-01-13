FROM python:3.12

WORKDIR /Microservices

COPY ../GitRepos/Projet5SDBD/ .

RUN pip install -r requirements.txt

EXPOSE 8081

CMD python3 services/FetchFutureDataService.py

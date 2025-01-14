FROM python:3.12

WORKDIR /StationService

COPY ../GitRepos/Projet5SDBD/StationService .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "StationService.py", ]
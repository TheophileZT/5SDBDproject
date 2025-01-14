FROM python:3.12

WORKDIR /FetchFutureDataService

COPY ../GitRepos/Projet5SDBD/FetchFutureDataService .

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python3", "FetchFutureDataService.py", ]
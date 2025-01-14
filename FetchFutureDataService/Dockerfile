FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY FetchFutureDataService.py .

RUN pip install -r requirements.txt

EXPOSE 5001

CMD python3 FetchFutureDataService.py

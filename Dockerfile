FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY services/FetchFutureDataService.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD python3 FetchFutureDataService.py

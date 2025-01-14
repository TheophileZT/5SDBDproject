FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY Inference.py .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python3 Inference.py

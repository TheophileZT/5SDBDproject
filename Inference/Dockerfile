# Build stage

FROM python:3.9 AS builder

WORKDIR /app

COPY requirements.txt .
COPY Inference.py .

RUN pip install -r requirements.txt

# Runtime stage

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY Inference.py .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD python3 Inference.py
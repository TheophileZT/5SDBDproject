FROM python:3.12

WORKDIR /Inference

COPY ../Projet5SDBD/Inference .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "Inference.py", ]

import requests
import os
from flask import Flask, jsonify

app = Flask(__name__)
port = int(os.environ.get('PORT', 5002))

@app.route("/")
def home():
    return "Hello, this is a Flask Microservice EventImpactScoringSystem!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
    
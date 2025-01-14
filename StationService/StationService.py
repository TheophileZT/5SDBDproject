from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 5003))

@app.route("/")
def home():
    return "Hello, this is a Flask Microservice StationService!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
    
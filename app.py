from flask import Flask, render_template, request,jsonify
from embeddings import create_and_store_embeddings,return_response
import logging
import requests

app = Flask(__name__)
app.config['db'] = create_and_store_embeddings()

@app.route("/")
def index():
    return render_template("index-old.html")


@app.route("/chat", methods=["POST"])
def chat():
    # Get the user input from the request
    print(app.config['db'])
    user_input = request.json['message']
    print(user_input)
    answer = return_response(user_input,app.config['db'])
    return str(answer)

if __name__ == "__main__":
    app.run(debug=True)


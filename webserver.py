from flask import Flask
from threading import Thread

app = Flask("webserver")

@app.route("/")
def home():
    return "Hi!"

def run():
    app.run(host = "0.0.0.0")

def start():
    thread = Thread(target = run)
    thread.start()